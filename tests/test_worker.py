from grader.worker import grade_problem


def test_grade_problem_returns_results():
    results = grade_problem("sum")
    assert results["compile"]["ok"]
    names = {t["name"] for t in results["tests"]}
    assert names == {"sum_visible", "sum_hidden", "sum_property"}
    assert "asan_ubsan" in results["sanitizers"]
    assert "hints" in results
