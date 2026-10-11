# Task API with SQLite Database

A RESTful API for managing a to-do list. Built with FastAPI (Python) and SQLite as part of the FlyRank Backend Track.

### Why SQLite?

- **Zero setup** - no separate database server needed
- **Single file** - entire database is one file (`tasks.db`)
- **Perfect for learning** - teaches SQL and database concepts without complexity
- **Production-ready for small apps** - used by Dropbox, Discord, and many others

### Where the Database File is Stored

The database file `tasks.db` is created automatically in your project root directory the first time you run the server. It contains:
- One table: `tasks` with columns: `id`, `title`, `done`
- Three example tasks inserted on first run
- All data persists across server restarts

## Installation & Running

1. Clone the repo and navigate to the folder
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install fastapi uvicorn[standard]`
5. Start the server: `uvicorn main:app --reload`
6. Visit `http://localhost:8000/docs` to see Swagger UI

The database file will be created automatically on first run.

## Endpoints

| HTTP Method | Endpoint | Description |
|-------------|----------|-------------|
| GET | `/` | Describe this API — name, version, and available endpoints |
| GET | `/health` | Check if the server is alive |
| GET | `/tasks` | Get all tasks from the database |
| GET | `/tasks/{id}` | Get a single task by ID |
| POST | `/tasks` | Create a new task with a title |
| PUT | `/tasks/{id}` | Update a task's title and/or done status |
| DELETE | `/tasks/{id}` | Delete a task by ID |

## Example: Create and Retrieve a Task

curl.exe -i -X POST http://localhost:8000/tasks -H “Content-Type: application/json” -d “{“title”:”Buy milk”}”

HTTP/1.1 201 Created
{“id”:4,”title”:”Buy milk”,”done”:false}

curl.exe -i http://localhost:8000/tasks/4

HTTP/1.1 200 OK
{“id”:4,”title”:”Buy milk”,”done”:false}


## Database Exploration with DB Browser

You can view and modify the database directly using **DB Browser for SQLite** (free download at `sqlitebrowser.org`):

1. Open DB Browser for SQLite
2. File → Open Database → select `tasks.db`
3. Click SQL Editor tab
4. Run SQL queries directly

### Example SQL Query

```sql
SELECT * FROM tasks WHERE done = 0;
```

This returns all incomplete tasks - the same data your API returns when you call `GET /tasks`.


## Architecture

**Week 2 (In-Memory):**
Client → API → Array in memory

**Week 3 (Database):**
Client → API → SQLite Database File


The API layer stayed the same; only the storage changed. Clients don't know or care - they send the same requests to the same endpoints.

## Notes

- Data is stored in `tasks.db` (SQLite file format)
- Database is automatically created if missing
- Example tasks are inserted only on first run
- All CRUD operations use SQL queries (no in-memory arrays)
- Changes via API or direct SQL are immediately visible in both places
