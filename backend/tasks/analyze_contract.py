from celery_worker import celery
from models.db import SessionLocal
from models.contract import Contract
from models.clause import Clause
from services.audit_service import log_event
from services.pdf_parser import extract_text_from_pdf
from services.llm_engine import extract_risk_clauses
from services.clause_retriever import find_relevant_sections

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_kwargs={"max_retries": 3}
)
def analyze_contract(self, contract_id: str):

    db = SessionLocal()

    try:
        logger.info(f"Starting analysis for {contract_id}")

        contract = db.query(Contract).filter(Contract.id == contract_id).first()

        if not contract:
            logger.error(f"Contract {contract_id} not found")
            return "Contract not found"

        # --------------------------------------------
        # RETRY LOGGING
        # --------------------------------------------
        if self.request.retries > 0:
            log_event(
                db,
                contract.id,
                "analysis_retry",
                "retrying",
                f"Retry attempt {self.request.retries}"
            )

        # --------------------------------------------
        # AUDIT — started
        # --------------------------------------------
        log_event(
            db,
            contract.id,
            "analysis_started",
            "processing",
            "Contract analysis started"
        )

        # --------------------------------------------
        # STEP 1 — Extract text
        # --------------------------------------------
        full_text = extract_text_from_pdf(contract.file_url)

        # --------------------------------------------
        # STEP 2 — Relevant sections
        # --------------------------------------------
        relevant_text = find_relevant_sections(full_text)

        if not relevant_text.strip():
            logger.warning(f"No relevant sections found for {contract_id}")
            relevant_text = full_text

        # --------------------------------------------
        # STEP 3 — AI
        # --------------------------------------------
        ai_result = extract_risk_clauses(relevant_text)

        if not isinstance(ai_result, dict):
            raise ValueError("AI returned invalid format")

        overall_score = ai_result.get("overall_risk_score", 0)

        # --------------------------------------------
        # STEP 4 — Persist Clause
        # --------------------------------------------
        existing_clause = (
            db.query(Clause)
            .filter(Clause.contract_id == contract.id)
            .first()
        )

        if existing_clause:
            existing_clause.risk_score = overall_score
            existing_clause.analysis_json = ai_result
        else:
            clause_entry = Clause(
                contract_id=contract.id,
                risk_score=overall_score,
                analysis_json=ai_result,
            )
            db.add(clause_entry)

        # --------------------------------------------
        # STEP 5 — Update Contract
        # --------------------------------------------
        contract.status = "completed"
        contract.risk_score = overall_score

        db.commit()

        # --------------------------------------------
        # AUDIT — success
        # --------------------------------------------
        log_event(
            db,
            contract.id,
            "analysis_completed",
            "success",
            f"Analysis completed with score {overall_score}"
        )

        logger.info(f"Completed analysis for {contract_id}")
        return "Analysis completed"

    except Exception as e:

        db.rollback()

        logger.error(f"Error analyzing {contract_id}: {str(e)}")

        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if contract:
            contract.status = "failed"
            db.commit()

        # --------------------------------------------
        # AUDIT — failure
        # --------------------------------------------
        log_event(
            db,
            contract_id,
            "analysis_failed",
            "error",
            str(e)
        )

        raise e

    finally:
        db.close()