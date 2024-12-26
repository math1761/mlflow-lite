from fastapi import FastAPI
from app.api.endpoints import models
from app.db.session import engine
from app.db.base import Base
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MLFlow Lite")

app.include_router(models.router, prefix="/api/v1")
