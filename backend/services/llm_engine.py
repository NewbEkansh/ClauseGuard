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


def normalize_clause(clause_data):
    if not clause_data:
        return None

    risk_level = clause_data.get("risk_level", "Low")

    return {
        "text": clause_data.get("text"),
        "risk_level": risk_level,
        "why_risky": clause_data.get("why_risky"),
        "scenario_analysis": clause_data.get("scenario_analysis"),
        "suggested_rewrite": clause_data.get("suggested_rewrite"),
        "score": RISK_MAP.get(risk_level, 20)
    }


def calculate_overall_score(clauses):
    scores = []

    for clause in clauses:
        if clause:
            scores.append(clause["score"])
        else:
            scores.append(10)

    return int(sum(scores) / len(scores))


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

        return {
            "overall_risk_score": overall_score,
            "termination_clause": termination,
            "indemnity_clause": indemnity,
            "liability_clause": liability,
            "non_compete_clause": non_compete
        }

    except Exception as e:
        return {
            "overall_risk_score": 0,
            "termination_clause": None,
            "indemnity_clause": None,
            "liability_clause": None,
            "non_compete_clause": None,
            "error": str(e)
        }