import time
from fastapi.testclient import TestClient
from api.main import app


def test_api_grade_flow():
    client = TestClient(app)
    resp = client.post("/grade/sum")
    assert resp.status_code == 200
    submission_id = resp.json()["submission_id"]

    res = client.get(f"/result/{submission_id}")
    data = res.json()
    assert data["results"]["compile"]["ok"]

    analytics = client.get("/analytics").json()
    assert analytics["total"] >= 1

    rj = client.post(f"/rejudge/{submission_id}")
    assert rj.status_code == 200
    assert rj.json()["submission_id"] != submission_id

    lb = client.get("/leaderboard/sum").json()
    assert lb and lb[0]["submission_id"] == submission_id


def test_api_exam_mode():
    client = TestClient(app)
    resp = client.post("/grade/sum?exam=true")
    assert resp.status_code == 200
    sid = resp.json()["submission_id"]
    res = client.get(f"/result/{sid}").json()
    assert res["results"]["exam_mode"] is True
