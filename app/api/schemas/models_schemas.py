from pydantic import BaseModel
from datetime import datetime

class ModelCreate(BaseModel):
    name: str
    version: str
    accuracy: float
    framework: str

class ModelVersionResponse(BaseModel):
    id: int
    name: str
    version: str
    accuracy: float
    created_at: datetime
    file_path = str

    class Config:
        from_attributes = True