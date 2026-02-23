from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.db import SessionLocal
from backend.models.contract import Contract
import os

router = APIRouter()


# ==============================
# DB Dependency
# ==============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==============================
# GET /contracts
# ==============================
@router.get("/contracts")
def list_contracts(db: Session = Depends(get_db)):

    contracts = (
        db.query(Contract)
        .order_by(Contract.created_at.desc())
        .all()
    )

    response = []

    for contract in contracts:

        # Extract only the filename from path
        base = os.path.basename(contract.file_url)

        # Remove UUID prefix if present
        clean_name = base.split("_", 1)[1] if "_" in base else base

        response.append({
            "id": str(contract.id),
            "file_name": clean_name,
            "status": contract.status,
            "created_at": contract.created_at.isoformat()
            if contract.created_at
            else None,
            "risk_score": contract.risk_score,
        })

    return response