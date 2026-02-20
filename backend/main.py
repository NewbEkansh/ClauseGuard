from fastapi import FastAPI
from backend.models.db import Base, engine
from backend.api.upload import router as upload_router
from backend.models.clause import Clause
app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(upload_router)

@app.get("/")
def root():
    return {"message": "ClauseGuard API Running"}
