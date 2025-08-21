from grader.similarity import checker
from grader.worker import grade_problem


def test_similarity_checker_basic():
    checker.submissions.clear()
    assert checker.check("int a;") == 0.0
    checker.register("s1", "int a;")
    assert checker.check("int a;") == 1.0


def test_exam_mode_runs_hidden_tests_only():
    res = grade_problem("sum", exam_mode=True)
    names = [t["name"] for t in res.get("tests", [])]
    assert names == ["sum_hidden"]
    assert res["exam_mode"] is True
