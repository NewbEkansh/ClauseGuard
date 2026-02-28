from fastapi import APIRouter, HTTPException
from models.db import SessionLocal
from models.clause import Clause
from models.contract import Contract
from fastapi.responses import StreamingResponse
from services.pdf_report import generate_pdf_report
import uuid

router = APIRouter()


@router.get("/analysis/{contract_id}")
def get_analysis(contract_id: str):
    db = SessionLocal()

    try:
        contract_uuid = uuid.UUID(contract_id)

        contract = db.query(Contract).filter(
            Contract.id == contract_uuid
        ).first()

        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        clause = db.query(Clause).filter(
            Clause.contract_id == contract_uuid
        ).first()

        if not clause:
            raise HTTPException(status_code=404, detail="Analysis not completed yet")

        return {
            "contract_id": contract_id,
            "status": contract.status,
            "risk_score": clause.analysis_json.get("overall_risk_score"),
            "analysis": clause.analysis_json
        }

    finally:
        db.close()


@router.get("/analysis/{contract_id}/report")
def download_report(contract_id: str):
    db = SessionLocal()

    try:
        contract_uuid = uuid.UUID(contract_id)

        clause = db.query(Clause).filter(
            Clause.contract_id == contract_uuid
        ).first()

        if not clause:
            raise HTTPException(status_code=404, detail="Analysis not found")

        pdf_buffer = generate_pdf_report(
            contract_id,
            clause.analysis_json
        )

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=analysis_{contract_id}.pdf"
            }
        )

    finally:
        db.close()