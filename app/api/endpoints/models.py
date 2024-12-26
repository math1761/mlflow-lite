import os
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from typing import List
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.api.schemas.models_schemas import ModelCreate, ModelVersionResponse
from app.db.session import get_db
from app.db.models import ModelVersion

router = APIRouter()
MODEL_STORAGE_DIR = os.getenv("MODEL_STORAGE_DIR", "./models")

@router.post("/models/", response_model=dict, summary="Add a new model version with file")
async def add_model_version(
    model: ModelCreate,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if model.framework not in ["onnx", "tensorflow", "sklearn"]:
        raise HTTPException(status_code=400, detail="Unsupported framework")
    
    existing_model = db.query(ModelVersion).filter(
        ModelVersion.name == model.name,
        ModelVersion.version == model.version
    ).first()
    if existing_model:
        raise HTTPException(status_code=400, detail="Model version already exists")

    model_dir = os.path.join(MODEL_STORAGE_DIR, model.name, model.version)
    os.makedirs(model_dir, exist_ok=True)
    file_path = os.path.join(model_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    new_model = ModelVersion(
        name=model.name,
        version=model.version,
        accuracy=model.accuracy,
        file_path=file_path,
        framework=model.framework
    )
    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    return {"message": "Model version added", "id": new_model.id, "file_path": file_path}

@router.get(
    "/models/",
    response_model=List[ModelVersionResponse],
    summary="List all model versions",
    responses={
        200: {
            "description": "List of model versions",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "model_A",
                            "version": "1.0",
                            "accuracy": 0.92,
                            "created_at": "2023-12-01T10:00:00"
                        }
                    ]
                }
            }
        }
    },
)
def list_models(db: Session = Depends(get_db)):
    models = db.query(ModelVersion).all()
    return models

@router.get("/models/{model_id}", response_model=ModelVersionResponse, summary="Get a model by ID")
def get_model(model_id: int, db: Session = Depends(get_db)):
    model = db.query(ModelVersion).filter(ModelVersion.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@router.get("/models/{model_id}/download/", summary="Download a model file")
def download_model(model_id: int, db: Session = Depends(get_db)):
    model = db.query(ModelVersion).filter(ModelVersion.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    if not os.path.exists(model.file_path):
        raise HTTPException(status_code=404, detail="Model file not found")
    return FileResponse(model.file_path, media_type="application/octet-stream", filename=os.path.basename(model.file_path))
