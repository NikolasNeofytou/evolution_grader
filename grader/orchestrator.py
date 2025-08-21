import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict

from .worker import grade_problem

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)


class Orchestrator:
    def __init__(self, max_workers: int = 2, retries: int = 1):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.retries = retries
        self.jobs: Dict[str, dict] = {}
        self.meta: Dict[str, str] = {}  # submission_id -> problem_id
        self.analytics_data = {"total": 0, "compile_fail": 0, "test_fail": 0}

    def submit(self, problem_id: str) -> str:
        submission_id = str(uuid.uuid4())

        def task():
            results = None
            for _ in range(self.retries + 1):
                results = grade_problem(problem_id)
                if results.get("compile", {}).get("ok", False):
                    break
            artifact = ARTIFACTS / f"{submission_id}.json"
            artifact.write_text(json.dumps(results))
            self.analytics_data["total"] += 1
            if not results.get("compile", {}).get("ok", False):
                self.analytics_data["compile_fail"] += 1
            elif any(t.get("status") != "passed" for t in results.get("tests", [])):
                self.analytics_data["test_fail"] += 1
            return {"submission_id": submission_id, "results": results}

        future = self.executor.submit(task)
        self.jobs[submission_id] = future
        self.meta[submission_id] = problem_id
        return submission_id

    def result(self, submission_id: str, wait: bool = True):
        fut = self.jobs.get(submission_id)
        if not fut:
            return None
        if wait:
            return fut.result()
        if fut.done():
            return fut.result()
        return {"status": "running"}

    def rejudge(self, submission_id: str) -> str:
        problem_id = self.meta.get(submission_id)
        if not problem_id:
            return ""
        return self.submit(problem_id)

    def analytics(self):
        return self.analytics_data


# create a global orchestrator instance
orchestrator = Orchestrator()

__all__ = ["orchestrator", "Orchestrator"]
