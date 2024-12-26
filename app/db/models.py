from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.db.base import Base

class ModelVersion(Base):
    __tablename__ = "model_versions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    accuracy = Column(Float, nullable=False)
    file_path = Column(String, nullable=False)
    framework = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
