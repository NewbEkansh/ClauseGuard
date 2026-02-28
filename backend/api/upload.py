from fastapi import APIRouter, UploadFile, File
from backend.models.db import SessionLocal
from backend.models.contract import Contract
from backend.tasks.analyze_contract import analyze_contract
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    db = SessionLocal()

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save file locally
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Store file path in DB
    new_contract = Contract(file_url=file_path, status="processing")
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)

    # Trigger async task
    analyze_contract.delay(str(new_contract.id))

    db.close()

    return {
        "message": "Contract uploaded",
        "contract_id": str(new_contract.id),
        "status": new_contract.status
    }