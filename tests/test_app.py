from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_predict_text_positive():
    r = client.post("/predict", json={"text": "this is great"})
    assert r.status_code == 200
    assert r.json()["prediction"] in [0, 1]


def test_predict_value_negative():
    r = client.post("/predict", json={"value": -1})
    assert r.status_code == 200
    assert r.json()["prediction"] == 0


def test_metrics_exposed():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "http_requests_total" in r.text
