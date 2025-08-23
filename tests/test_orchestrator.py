import time
from grader.orchestrator import Orchestrator


def test_orchestrator_submit_and_result():
    orch = Orchestrator(max_workers=1)
    sub_id = orch.submit("sum")
    res = orch.result(sub_id)
    assert res["results"]["compile"]["ok"]
    assert "similarity" in res["results"]
    assert orch.analytics()["total"] == 1
    new_id = orch.rejudge(sub_id)
    assert new_id != sub_id
