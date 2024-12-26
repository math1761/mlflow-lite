def test_add_model(client):
    response = client.post(
        "/api/v1/models/",
        json={
            "name": "model_A",
            "version": "1.0",
            "accuracy": 0.92
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Model version added"
    assert "id" in data

def test_list_models(client):
    client.post("/api/v1/models/", json={"name": "model_A", "version": "1.0", "accuracy": 0.92})
    client.post("/api/v1/models/", json={"name": "model_B", "version": "1.1", "accuracy": 0.85})

    response = client.get("/api/v1/models/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "model_A"
    assert data[1]["name"] == "model_B"

def test_get_model_by_id(client):
    response = client.post(
        "/api/v1/models/",
        json={"name": "model_A", "version": "1.0", "accuracy": 0.92}
    )
    model_id = response.json()["id"]

    response = client.get(f"/api/v1/models/{model_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "model_A"
    assert data["version"] == "1.0"
    assert data["accuracy"] == 0.92

def test_add_duplicate_model(client):
    client.post(
        "/api/v1/models/",
        json={"name": "model_A", "version": "1.0", "accuracy": 0.92}
    )
    response = client.post(
        "/api/v1/models/",
        json={"name": "model_A", "version": "1.0", "accuracy": 0.93}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Model version already exists"

def test_get_nonexistent_model(client):
    response = client.get("/api/v1/models/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Model not found"

def test_upload_model(client):
    file_path = "/path/to/dummy_model.pkl"
    with open(file_path, "wb") as f:
        f.write(b"dummy model content")
    
    with open(file_path, "rb") as f:
        response = client.post(
            "/api/v1/models/",
            data={"name": "model_A", "version": "1.0", "accuracy": 0.92},
            files={"file": f}
        )
    
    assert response.status_code == 200
    assert response.json()["file_path"] is not None

def test_health_endpoint(client):
    response = client.get("/api/v1/models/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
