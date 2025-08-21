from grader.worker import grade_problem


def test_grade_python_problem():
    res = grade_problem("py_sum")
    assert res["compile"]["ok"]
    assert all(t["status"] == "passed" for t in res["tests"])
