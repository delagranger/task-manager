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

@app.get("/groups")
def get_groups():
    return tm.list_groups(
        sort_type="id"
    )
