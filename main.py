from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = [
    {"id": 1, "title": "Get Chocolate", "done": True},
    {"id": 2, "title": "Coffee Date", "done": False},
    {"id": 3, "title": "Buy Gift", "done": False}
]

@app.get("/")
def read_root():
    """Describe this API - name, version, and available endpoints.""" 
    return {
        "name": "Task API", 
        "version": "1.0", 
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    """Check if the server is alive"""
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    """Get all tasks."""
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Get a single task by ID."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=201)
def create_task(task_data: dict):
    """Create a new task with a title."""
    # Validate: title must exist and not be empty
    if "title" not in task_data or not task_data["title"] or not task_data["title"].strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: dict):
    """Update a task's title with done status."""
    # Find the task
    for task in tasks:
        if task["id"] == task_id:
            # Validate if title is provided
            if "title" in task_data:
                if not task_data["title"] or not task_data["title"].strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = task_data["title"].strip()
            
            # Update done flag if provided
            if "done" in task_data:
                task["done"] = task_data["done"]
            
            return task
    
    # Task not found
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task by ID."""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return  # 204 No Content — just return empty
    
    # Task not found
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
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