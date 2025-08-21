from grader.orchestrator import orchestrator


def test_leaderboard_tracks_scores():
    sid = orchestrator.submit("sum")
    orchestrator.result(sid)  # wait for completion
    board = orchestrator.leaderboard("sum")
    assert any(entry["submission_id"] == sid for entry in board)
    assert any(entry["score"] == 100 for entry in board)
