# Basic Authentication

## Tasks

### Task 0
Download project startup zip

### Task 1
Edit `api/v1/app.py`:
- Add a new error handler for this status code, the response must be:
	- a JSON: `{"error": "Unauthorized"}`
	- status code `401`
	- you must use `jsonify` from Flask

For testing this new error handler, add a new endpoint in `api/v1/views/index.py`:
- Route: `GET /api/v1/unauthorized`
- This endpoint must raise a 401 error by using `abort`

### Task 2
Edit `api/v1/app.py`:
- Add a new error handler for this status code, the response must be:
	- a JSON: `{"error": "Forbidden"}`
	- status code `403`
	- you must use `jsonify` from Flask

For testing this new error handler, add a new endpoint in `api/v1/views/index.py`:
- Route: `GET /api/v1/forbidden`
- This endpoint must raise a 403 error by using `abort`
