from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.auth_service import authenticate_admin, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginRequest):

    if not authenticate_admin(data.username, data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": data.username})

    return {"access_token": token, "token_type": "bearer"}