from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import ModelVersion
from typing import Any, Dict
import os
import onnxruntime as ort
import tensorflow as tf
import joblib

router = APIRouter()

# Directory for storing models
MODEL_STORAGE_PATH = "/app/models"

def get_model_file_path(name: str, version: str) -> str:
    """
    Construct the file path for a stored model.
    """
    return os.path.join(MODEL_STORAGE_PATH, f"{name}_{version}")

def load_onnx_model(model_path: str):
    """
    Load an ONNX model from the given path.
    """
    try:
        return ort.InferenceSession(model_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load ONNX model: {str(e)}")

def load_tensorflow_model(model_path: str):
    """
    Load a TensorFlow model from the given path.
    """
    try:
        return tf.keras.models.load_model(model_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load TensorFlow model: {str(e)}")

def load_sklearn_model(model_path: str):
    """
    Load a scikit-learn model from the given path.
    """
    try:
        return joblib.load(model_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load scikit-learn model: {str(e)}")

@router.post("/models/{model_id}/predict", response_model=Dict[str, Any])
def predict_model_by_id(model_id: int, input_data: Any, db: Session = Depends(get_db)):
    """
    Perform prediction using a model identified by its ID.
    """
    model = db.query(ModelVersion).filter(ModelVersion.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    model_file_path = get_model_file_path(model.name, model.version)
    if not os.path.exists(model_file_path):
        raise HTTPException(status_code=500, detail="Model file not found")

    if model.framework == "onnx":
        session = load_onnx_model(model_file_path)
        input_name = session.get_inputs()[0].name
        try:
            prediction = session.run(None, {input_name: input_data})
            return {"prediction": prediction}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    elif model.framework == "tensorflow":
        loaded_model = load_tensorflow_model(model_file_path)
        try:
            prediction = loaded_model.predict(input_data).tolist()
            return {"prediction": prediction}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    elif model.framework == "sklearn":
        loaded_model = load_sklearn_model(model_file_path)
        try:
            prediction = loaded_model.predict(input_data).tolist()
            return {"prediction": prediction}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Unsupported framework")

@router.post("/predict", response_model=Dict[str, Any])
def predict_model(data: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Perform prediction using a model identified by its name and version.
    """
    model_name = data.get("model_name")
    version = data.get("version")
    input_data = data.get("data")

    if not model_name or not version or input_data is None:
        raise HTTPException(
            status_code=400,
            detail="Request must include 'model_name', 'version', and 'data'",
        )

    model = db.query(ModelVersion).filter(
        ModelVersion.name == model_name, ModelVersion.version == version
    ).first()

    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    model_file_path = get_model_file_path(model.name, model.version)
    if not os.path.exists(model_file_path):
        raise HTTPException(status_code=500, detail="Model file not found")

    if model.framework == "onnx":
        session = load_onnx_model(model_file_path)
        input_name = session.get_inputs()[0].name
        try:
            predictions = session.run(None, {input_name: input_data})
            return {"predictions": predictions}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    elif model.framework == "tensorflow":
        loaded_model = load_tensorflow_model(model_file_path)
        try:
            predictions = loaded_model.predict(input_data).tolist()
            return {"predictions": predictions}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    elif model.framework == "sklearn":
        loaded_model = load_sklearn_model(model_file_path)
        try:
            predictions = loaded_model.predict(input_data).tolist()
            return {"predictions": predictions}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Unsupported framework")
