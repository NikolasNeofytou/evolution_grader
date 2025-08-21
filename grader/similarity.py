import difflib
from typing import Dict


class SimilarityChecker:
    """Naive in-memory similarity tracker using SequenceMatcher."""

    def __init__(self):
        self.submissions: Dict[str, str] = {}

    def register(self, submission_id: str, code: str) -> None:
        self.submissions[submission_id] = code

    def check(self, code: str) -> float:
        if not self.submissions:
            return 0.0
        return max(
            difflib.SequenceMatcher(None, code, prev).ratio()
            for prev in self.submissions.values()
        )


# global instance used by the orchestrator
checker = SimilarityChecker()

__all__ = ["checker", "SimilarityChecker"]
