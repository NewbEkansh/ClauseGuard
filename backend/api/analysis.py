from fastapi import APIRouter, HTTPException
from backend.models.db import SessionLocal
from backend.models.clause import Clause
from backend.models.contract import Contract
import uuid

router = APIRouter()


@router.get("/analysis/{contract_id}")
def get_analysis(contract_id: str):
    db = SessionLocal()

    try:
        contract_uuid = uuid.UUID(contract_id)

        contract = db.query(Contract).filter(Contract.id == contract_uuid).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        clause = db.query(Clause).filter(Clause.contract_id == contract_uuid).first()
        if not clause:
            raise HTTPException(status_code=404, detail="Analysis not completed yet")

        return {
            "contract_id": contract_id,
            "status": contract.status,
            "risk_score": clause.risk_score,
            "analysis": clause.analysis_json
        }

    finally:
        db.close()