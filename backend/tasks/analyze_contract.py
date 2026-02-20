from backend.celery_worker import celery
from backend.models.db import SessionLocal
from backend.models.contract import Contract
from backend.models.clause import Clause
from backend.services.pdf_parser import extract_text_from_pdf
from backend.services.llm_engine import extract_risk_clauses
from backend.services.clause_retriever import find_relevant_sections


@celery.task
def analyze_contract(contract_id: str):
    db = SessionLocal()

    try:
        contract = db.query(Contract).filter(Contract.id == contract_id).first()

        if not contract:
            return "Contract not found"

        # STEP 1 — Extract full contract text
        full_text = extract_text_from_pdf(contract.file_url)
        print("Full Text Preview:", full_text[:1000])

        # STEP 2 — Retrieve only relevant sections
        relevant_text = find_relevant_sections(full_text)

        print("Relevant Text Preview:", relevant_text[:1000])

        # Safety fallback (if keyword search fails)
        if not relevant_text.strip():
            print("No relevant sections found — using full text.")
            relevant_text = full_text

        # STEP 3 — Run AI only on relevant text
        ai_result = extract_risk_clauses(relevant_text)

        print("AI Result:", ai_result)

        # STEP 4 — Persist AI output
        clause_entry = Clause(
            contract_id=contract.id,
            termination_clause=ai_result.get("termination_clause"),
            indemnity_clause=ai_result.get("indemnity_clause"),
            liability_clause=ai_result.get("liability_clause"),
            non_compete_clause=ai_result.get("non_compete_clause"),
            risk_score=ai_result.get("risk_score"),
        )

        db.add(clause_entry)

        # STEP 5 — Update contract status
        contract.status = "completed"

        db.commit()

        return "Analysis completed"

    except Exception as e:
        db.rollback()

        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if contract:
            contract.status = "failed"
            db.commit()

        print("AI Error:", str(e))
        raise e

    finally:
        db.close()