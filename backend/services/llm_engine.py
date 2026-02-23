import json
import random
import re
from groq import Groq
from backend.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def extract_risk_clauses(contract_text: str):

    # ---- DEV MODE ----
    if settings.DEV_MODE:
        return {
            "termination_clause": "Either party may terminate with 30 days written notice.",
            "indemnity_clause": "Client agrees to indemnify the service provider from claims.",
            "liability_clause": "Liability is limited to the total value of the contract.",
            "non_compete_clause": "Employee may not engage in competing business for 12 months.",
            "risk_score": random.randint(30, 70),
            "mock": True
        }

    prompt = f"""
You are an expert legal contract risk analyst.

For each clause below:
1. Extract the exact clause text (or null if not present).
2. Assign a risk_level: Low, Medium, or High.
3. Explain why it may be risky.
4. Provide a real-world scenario explaining the risk exposure.
5. Suggest a safer alternative rewrite.

Clauses to analyze:
- termination
- indemnity
- liability
- non_compete

Return ONLY valid JSON in this exact format:

{{
  "termination": {{
    "text": string | null,
    "risk_level": "Low | Medium | High",
    "why_risky": string,
    "scenario_analysis": string,
    "suggested_rewrite": string
  }},
  "indemnity": {{ ... }},
  "liability": {{ ... }},
  "non_compete": {{ ... }},
  "overall_risk_score": integer
}}

Contract:
{contract_text}
"""

    try:
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )

        content = response.choices[0].message.content.strip()

        # ---- Extract JSON safely ----
        # Handles cases where model wraps JSON in text or markdown blocks
        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON object found in model output")

        json_text = json_match.group()

        return json.loads(json_text)

    except Exception as e:
        return {
            "termination_clause": None,
            "indemnity_clause": "",
            "liability_clause": "",
            "non_compete_clause": "",
            "risk_score": 0,
            "error": str(e),
            "provider": "groq"
        }