from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_research_empty_topic():
    response = client.post("/research", data={"topic": ""})
    assert response.status_code in [422, 500]
