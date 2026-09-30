# Task API

A simple RESTful API for managing a to-do list. Built with FastAPI and Python as part of the FlyRank Backend Track Assignment.

## Installation & Running

1. Clone the repo and navigate to the folder
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install fastapi uvicorn[standard]`
5. Start the server: `uvicorn main:app --reload`
6. Visit `http://localhost:8000/docs` to see Swagger UI

## Endpoints

| HTTP Method | Endpoint | Description |
|-------------|----------|-------------|
| GET | `/` | Describe this API — name, version, and available endpoints |
| GET | `/health` | Check if the server is alive |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get a single task by ID |
| POST | `/tasks` | Create a new task with a title |
| PUT | `/tasks/{id}` | Update a task's title and/or done status |
| DELETE | `/tasks/{id}` | Delete a task by ID |

## Example Request & Response
curl.exe -i http://localhost:8000/tasks/1

HTTP/1.1 200 OK
date: Wed, 30 Sep 2026 10:08:47 GMT
server: uvicorn
content-length: 46
content-type: application/json

{"id":1,"title":"Buy Chocolate","done":true}

## Swagger UI

The API includes interactive API documentation at `http://localhost:8000/docs` - test all endpoints with the "Try it out" button without writing curl commands.

## Notes
- Data is stored in memory only - restarting the server resets all tasks to the default 3 examples
- All responses are JSON
- Invalid requests (missing title, wrong ID) return appropriate error codes (400, 404)