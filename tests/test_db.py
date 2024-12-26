def test_table_creation(db_session):
    from sqlalchemy import inspect
    inspector = inspect(db_session.bind)
    tables = inspector.get_table_names()
    assert "model_versions" in tables

def test_insert_data(db_session):
    from app.db.models import ModelVersion

    new_model = ModelVersion(name="model_A", version="1.0", accuracy=0.92)
    db_session.add(new_model)
    db_session.commit()

    result = db_session.query(ModelVersion).filter_by(name="model_A", version="1.0").first()
    assert result is not None
    assert result.name == "model_A"