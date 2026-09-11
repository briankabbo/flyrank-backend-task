from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = [
    {"id": 1, "title": "Get Chocolate", "done": True},
    {"id": 2, "title": "Coffee Date", "done": False},
    {"id": 3, "title": "Buy Gift", "done": False}
]

@app.get("/")
def read_root():
    return {
        "name": "Task API", 
        "version": "1.0", 
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=201)
def create_task(task_data: dict):
    # Validate: title must exist and not be empty
    if "title" not in task_data or not task_data["title"] or not task_data["title"].strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")
    
    # Generate next ID
    next_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    
    # Create new task with done = False by default
    new_task = {
        "id": next_id,
        "title": task_data["title"].strip(),
        "done": False
    }
    
    # Add to list
    tasks.append(new_task)
    
    # Return the created task
    return new_task