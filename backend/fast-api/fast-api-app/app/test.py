from fastapi import FastAPI, HTTPException

app = FastAPI(title = "my backend app", description="backend app", version = "1.1.0")

@app.get("/")
def baseRoute():
    return { "status": "ok" }

@app.get("/health", status_code = 204)
def healthCheck():
    return { "status": "ok" }

tasks = [ 
    {
        "id": 1,
        "name": "Task 1"
    },
    {
        "id": 2,
        "name": "Task 2"
    }
]

@app.get("/tasks/{taskId}")
def getTasks(taskId: int):
    for task in tasks:
        if (task["id"] == taskId):
            return task
    raise HTTPException(status_code = 404, detail = "Task not found")