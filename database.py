import sqlite3

DATABASE = "tasks.db"

def init_db():
    """Create the database and tables if they don't exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tasks table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    
    # Check if table is empty, if so insert example tasks
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    if count == 0:
        cursor.executemany("""
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
        """, [
            ("Buy milk", 0),
            ("Walk the dog", 1),
            ("Finish assignment", 0),
        ])
    
    conn.commit()
    conn.close()

def get_all_tasks():
    """Fetch all tasks from the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Returns rows as dicts
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tasks

def get_task_by_id(task_id: int):
    """Fetch a single task by ID."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_task(title: str):
    """Insert a new task into the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
    """, (title, 0))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return {"id": task_id, "title": title, "done": False}

def update_task(task_id: int, title: str = None, done: bool = None):
    """Update a task's title and/or done status."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Check if task exists first
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        conn.close()
        return None  # Task not found
    
    # Build dynamic update query
    updates = []
    params = []
    
    if title is not None:
        updates.append("title = ?")
        params.append(title)
    
    if done is not None:
        updates.append("done = ?")
        params.append(done)
    
    if not updates:
        conn.close()
        return None  # Nothing to update
    
    params.append(task_id)
    query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    
    # Fetch and return the updated task
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    conn.row_factory = sqlite3.Row
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def delete_task(task_id: int):
    """Delete a task by ID."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Check if task exists
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        conn.close()
        return False  # Task not found
    
    # Delete it
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return True  # Success