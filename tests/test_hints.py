from grader.worker import _collect_hints


def test_collect_hints_matches_patterns():
    logs = "warning: something bad\nAddressSanitizer: heap-use-after-free"
    hints = _collect_hints(logs)
    assert any("compiler warnings" in h for h in hints)
    assert any("memory error" in h for h in hints)
