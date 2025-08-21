from fastapi import FastAPI
from grader.orchestrator import orchestrator

app = FastAPI()


@app.post("/grade/{problem_id}")
async def grade(problem_id: str):
    submission_id = orchestrator.submit(problem_id)
    return {"submission_id": submission_id}


@app.get("/result/{submission_id}")
async def result(submission_id: str):
    res = orchestrator.result(submission_id)
    if res is None:
        return {"error": "unknown submission"}
    return res


@app.post("/rejudge/{submission_id}")
async def rejudge(submission_id: str):
    new_id = orchestrator.rejudge(submission_id)
    return {"submission_id": new_id}


@app.get("/analytics")
async def analytics():
    return orchestrator.analytics()
