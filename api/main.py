from fastapi import FastAPI
from grader.worker import grade_problem

app = FastAPI()


@app.post("/grade/{problem_id}")
async def grade(problem_id: str):
    return grade_problem(problem_id)
