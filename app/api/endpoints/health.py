from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import ModelVersion
from typing import Any
import pickle
import onnxruntime as ort
import os

router = APIRouter()

MODEL_STORAGE_PATH = "/app/models"

@router.get("/models/{model_id}/health", response_model=dict)
def check_model_health(model_id: int, db: Session = Depends(get_db)):
    model = db.query(ModelVersion).filter(ModelVersion.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    model_file_path = os.path.join(MODEL_STORAGE_PATH, f"{model.name}_{model.version}.onnx")
    if not os.path.exists(model_file_path):
        raise HTTPException(status_code=500, detail="Model file not found")
    
    try:
        ort.InferenceSession(model_file_path)
        return {"status": "healthy", "message": "Model is ready"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model loading failed: {str(e)}")