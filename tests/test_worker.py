from grader.worker import grade_problem


def test_grade_problem_returns_results():
    results = grade_problem("sum")
    assert results["compile"]["ok"]
    assert any(t["name"] == "Sum.Small" for t in results["tests"])
    assert "asan_ubsan" in results["sanitizers"]
