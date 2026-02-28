from fastapi import FastAPI
from models.db import Base, engine
from api.upload import router as upload_router
from models.clause import Clause
from api.analysis import router as analysis_router
from fastapi.middleware.cors import CORSMiddleware
from api.contracts import router as contracts_router
from api.admin import router as admin_router
from api.auth import router as auth_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(analysis_router)
app.include_router(admin_router)
app.include_router(auth_router)
Base.metadata.create_all(bind=engine)
app.include_router(upload_router)
app.include_router(contracts_router)
@app.get("/")
def root():
    return {"message": "ClauseGuard API Running"}
