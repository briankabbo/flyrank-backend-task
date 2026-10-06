import sqlite3
import os

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