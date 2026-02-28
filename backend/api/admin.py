from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from backend.models.db import SessionLocal
from backend.models.contract import Contract
from backend.models.audit_log import AuditLog
from backend.services.auth_service import verify_token
from backend.models.clause import Clause

router = APIRouter(prefix="/admin", tags=["Admin"])

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------
# JWT Protection Dependency
# --------------------------------------------
def admin_required(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


# --------------------------------------------
# Admin Stats
# --------------------------------------------
@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    total = db.query(func.count(Contract.id)).scalar()
    completed = db.query(func.count(Contract.id)).filter(
        Contract.status == "completed"
    ).scalar()
    failed = db.query(func.count(Contract.id)).filter(
        Contract.status == "failed"
    ).scalar()
    processing = db.query(func.count(Contract.id)).filter(
        Contract.status == "processing"
    ).scalar()

    avg_score = db.query(func.avg(Contract.risk_score)).scalar() or 0

    return {
        "total_contracts": total,
        "completed": completed,
        "failed": failed,
        "processing": processing,
        "average_risk_score": round(float(avg_score), 2)
    }


# --------------------------------------------
# Contract List (with filters + pagination)
# --------------------------------------------
@router.get("/contracts")
def list_contracts(
    status: Optional[str] = Query(None),
    min_score: Optional[int] = Query(None),
    max_score: Optional[int] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    query = db.query(Contract)

    if status:
        query = query.filter(Contract.status == status)

    if min_score is not None:
        query = query.filter(Contract.risk_score >= min_score)

    if max_score is not None:
        query = query.filter(Contract.risk_score <= max_score)

    contracts = (
        query
        .order_by(Contract.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [
        {
            "id": str(c.id),
            "status": c.status,
            "risk_score": c.risk_score,
            "created_at": c.created_at
        }
        for c in contracts
    ]


# --------------------------------------------
# Single Contract Detail
# --------------------------------------------
@router.get("/contracts/{contract_id}")
def get_contract_detail(
    contract_id: str,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    contract = db.query(Contract).filter(
        Contract.id == contract_id
    ).first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    clause = db.query(Clause).filter(
        Clause.contract_id == contract.id
    ).first()

    return {
        "id": str(contract.id),
        "status": contract.status,
        "risk_score": contract.risk_score,
        "file_url": contract.file_url,
        "created_at": contract.created_at,
        "analysis": clause.analysis_json if clause else None
    }


# --------------------------------------------
# Audit Logs
# --------------------------------------------
@router.get("/audit")
def get_audit_logs(
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "contract_id": str(log.contract_id),
            "action": log.action,
            "status": log.status,
            "message": log.message,
            "created_at": log.created_at
        }
        for log in logs
    ]
    # --------------------------------------------
    # Contract-specific Audit Logs
    # --------------------------------------------
@router.get("/contracts/{contract_id}/audit")
def get_contract_audit(
    contract_id: str,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    logs = (
        db.query(AuditLog)
        .filter(AuditLog.contract_id == contract_id)
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    return [
        {
            "action": log.action,
            "status": log.status,
            "message": log.message,
            "created_at": log.created_at
        }
        for log in logs
    ]