from backend.celery_worker import celery
from backend.models.db import SessionLocal
from backend.models.contract import Contract
from backend.models.clause import Clause
from backend.services.pdf_parser import extract_text_from_pdf
from backend.services.llm_engine import extract_risk_clauses
from backend.services.clause_retriever import find_relevant_sections


@celery.task
def analyze_contract(contract_id: str):

    # --------------------------------------------
    # Create DB session inside Celery worker
    # --------------------------------------------
    db = SessionLocal()

    try:
        # --------------------------------------------
        # STEP 0 — Fetch contract
        # --------------------------------------------
        contract = db.query(Contract).filter(Contract.id == contract_id).first()

        if not contract:
            return "Contract not found"

        # --------------------------------------------
        # STEP 1 — Extract full contract text
        # --------------------------------------------
        full_text = extract_text_from_pdf(contract.file_url)
        print("Full Text Preview:", full_text[:1000])

        # --------------------------------------------
        # STEP 2 — Retrieve only relevant sections
        # --------------------------------------------
        relevant_text = find_relevant_sections(full_text)
        print("Relevant Text Preview:", relevant_text[:1000])

        # Safety fallback (if keyword search fails)
        if not relevant_text.strip():
            print("No relevant sections found — using full text.")
            relevant_text = full_text

        # --------------------------------------------
        # STEP 3 — Run AI on relevant text
        # --------------------------------------------
        ai_result = extract_risk_clauses(relevant_text)
        print("AI Result:", ai_result)

        overall_score = ai_result.get("overall_risk_score", 0)

        # --------------------------------------------
        # STEP 4 — Persist / Update Clause row
        # --------------------------------------------

        existing_clause = (
            db.query(Clause)
            .filter(Clause.contract_id == contract.id)
            .first()
        )

        if existing_clause:
            # Update existing analysis
            existing_clause.risk_score = overall_score
            existing_clause.analysis_json = ai_result
        else:
            # Create new analysis entry
            clause_entry = Clause(
                contract_id=contract.id,
                risk_score=overall_score,
                analysis_json=ai_result,
            )
            db.add(clause_entry)

        # --------------------------------------------
        # STEP 5 — Update Contract table
        # --------------------------------------------
        contract.status = "completed"

        # 🔥 THIS FIXES YOUR NULL ISSUE
        contract.risk_score = overall_score

        db.commit()

        return "Analysis completed"

    except Exception as e:

        db.rollback()

        # Mark contract as failed
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if contract:
            contract.status = "failed"
            db.commit()

        print("AI Error:", str(e))
        raise e

    finally:
        db.close()