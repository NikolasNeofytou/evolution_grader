from grader.worker import grade_problem


def test_grade_project_problem():
    res = grade_problem("sum_project")
    assert res["compile"]["ok"]
    names = {t["name"] for t in res["tests"]}
    assert names == {"sum_visible", "sum_hidden"}
