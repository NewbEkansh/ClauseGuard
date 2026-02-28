import json
import re
from groq import Groq
from backend.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)


RISK_MAP = {
    "Low": 20,
    "Medium": 50,
    "High": 80,
    "Extreme": 95
}
RED_FLAG_KEYWORDS = [
    "sole discretion",
    "without notice",
    "unlimited liability",
    "perpetual",
    "irrevocable",
    "indemnify and hold harmless",
    "no liability",
    "exclusive remedy"
]

RED_FLAG_BOOST = 10

def detect_red_flags(text: str):
    if not text:
        return 0

    text_lower = text.lower()
    boost = 0

    for keyword in RED_FLAG_KEYWORDS:
        if keyword in text_lower:
            boost += RED_FLAG_BOOST

    return boost

def normalize_clause(clause_data):
    if not clause_data:
        return None

    risk_level = clause_data.get("risk_level", "Low")
    base_score = RISK_MAP.get(risk_level, 20)

    text = clause_data.get("text")

    red_flag_bonus = detect_red_flags(text)

    final_score = min(base_score + red_flag_bonus, 100)

    return {
        "text": text,
        "risk_level": risk_level,
        "why_risky": clause_data.get("why_risky"),
        "scenario_analysis": clause_data.get("scenario_analysis"),
        "suggested_rewrite": clause_data.get("suggested_rewrite"),
        "score": final_score,
        "red_flag_bonus": red_flag_bonus
    }


def calculate_overall_score(clauses):
    scores = []

    for clause in clauses:
        if clause:
            scores.append(clause["score"])
        else:
            scores.append(10)

    return int(sum(scores) / len(scores))

def detect_asymmetry(termination, indemnity, liability):
    asymmetry_boost = 0

    if indemnity and liability:
        indemnity_text = indemnity["text"].lower() if indemnity["text"] else ""
        liability_text = liability["text"].lower() if liability["text"] else ""

        if "indemnify" in indemnity_text and "limit" in liability_text:
            asymmetry_boost += 10

    if termination:
        termination_text = termination["text"].lower() if termination["text"] else ""

        if "sole discretion" in termination_text:
            asymmetry_boost += 10

    return asymmetry_boost

def extract_risk_clauses(contract_text: str):

    prompt = f"""
You are an expert legal contract risk analyst.

For each of the following clauses:
1. Termination
2. Indemnity
3. Limitation of Liability
4. Non-Compete

If the clause exists:
- Extract the exact clause text.
- Assign a risk_level: Low, Medium, High, or Extreme.
- Explain why it is risky.
- Provide a realistic scenario analysis.
- Suggest a safer rewrite.

If the clause does NOT exist, return null.

Return ONLY valid JSON in this format:

{{
  "termination_clause": {{
    "text": "...",
    "risk_level": "Low|Medium|High|Extreme",
    "why_risky": "...",
    "scenario_analysis": "...",
    "suggested_rewrite": "..."
  }} | null,

  "indemnity_clause": {{ ... }} | null,
  "liability_clause": {{ ... }} | null,
  "non_compete_clause": {{ ... }} | null
}}

Contract:
{contract_text}
"""

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        content = response.choices[0].message.content.strip()
        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON returned from model")

        parsed = json.loads(json_match.group())

        termination = normalize_clause(parsed.get("termination_clause"))
        indemnity = normalize_clause(parsed.get("indemnity_clause"))
        liability = normalize_clause(parsed.get("liability_clause"))
        non_compete = normalize_clause(parsed.get("non_compete_clause"))

        overall_score = calculate_overall_score([
            termination,
            indemnity,
            liability,
            non_compete
        ])
        asymmetry_boost = detect_asymmetry(
            termination,
            indemnity,
            liability
        )
        overall_score=min(overall_score + asymmetry_boost, 100)

        return {
            "overall_risk_score": overall_score,
            "termination_clause": termination,
            "indemnity_clause": indemnity,
            "liability_clause": liability,
            "non_compete_clause": non_compete
        }

    except Exception as e:
        return {
        "overall_risk_score": overall_score,
        "asymmetry_bonus": asymmetry_bonus,
        "termination_clause": termination,
        "indemnity_clause": indemnity,
        "liability_clause": liability,
        "non_compete_clause": non_compete
        }