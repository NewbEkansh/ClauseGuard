from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from backend.models.db import Base
import uuid


class Clause(Base):
    __tablename__ = "clauses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"))

    termination_clause = Column(String)
    indemnity_clause = Column(String)
    liability_clause = Column(String)
    non_compete_clause = Column(String)

    risk_score = Column(Integer)