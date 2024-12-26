import os

DB_URL = os.getenv("DATABASE_URL")

class Settings:
    PROJECT_NAME: str = "MLFlow Lite"
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL")

settings = Settings()
