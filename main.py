from fastapi import FastAPI, HTTPException
from database import init_db, get_all_tasks, get_task_by_id, create_task, update_task, delete_task

app = FastAPI()

init_db()

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
    """Check if the server is alive."""
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks_endpoint():
    """Get all tasks."""
    return get_all_tasks()

@app.get("/tasks/{task_id}")
def get_task_endpoint(task_id: int):
    """Get a single task by ID."""
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

@app.post("/tasks", status_code=201)
def create_task_endpoint(task_data: dict):
    """Create a new task with a title."""
    # Validate: title must exist and not be empty
    if "title" not in task_data or not task_data["title"] or not task_data["title"].strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")
    
    new_task = create_task(task_data["title"].strip())
    return new_task

@app.put("/tasks/{task_id}")
def update_task_endpoint(task_id: int, task_data: dict):
    """Update a task's title and/or done status."""
    # Extract title and done from request if provided
    title = task_data.get("title")
    done = task_data.get("done")
    
    # Validate title if provided
    if title is not None and (not title or not title.strip()):
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    # Update in database
    updated_task = update_task(task_id, title.strip() if title else None, done)
    
    if not updated_task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task_endpoint(task_id: int):
    """Delete a task by ID."""
    success = delete_task(task_id)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")