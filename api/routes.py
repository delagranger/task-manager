from fastapi import FastAPI

from services import TaskManager

app = FastAPI()

tm = TaskManager()


@app.get("/tasks")
def get_tasks():
    return tm.list_tasks(
        sort_type="id",
        filtered=True,
        status="active",
        group=""
    )