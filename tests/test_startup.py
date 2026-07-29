from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_app_imports_and_starts():
    assert app is not None

def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200