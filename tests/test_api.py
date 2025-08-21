from fastapi.testclient import TestClient
from api.main import app


def test_api_grade_endpoint():
    client = TestClient(app)
    resp = client.post("/grade/sum")
    assert resp.status_code == 200
    body = resp.json()
    assert body["compile"]["ok"]
