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

### Task 3
Create a class to manage the API authentication.
- Create a folder `api/v1/auth`
- Create an empty file `api/v1/auth/__init__.py`
- Create the class `Auth`:
	- in the file `api/v1/auth/auth.py`
	- import `request` from `flask`
	- class name `Auth`
	- public method `def require_auth(self, path: str, excluded_paths: List[str]) -> bool:` that returns `False` - `path` and `excluded_paths` will be used later, now, you don’t need to take care of them
	- public method `def authorization_header(self, request=None) -> str:` that returns `None` - `request` will be the Flask request object
	- public method `def current_user(self, request=None) -> TypeVar('User'):` that returns `None` - `request` will be the Flask request object

This class is the template for all authentication system you will implement.

### Task 4
Update the method `def require_auth(self, path: str, excluded_paths: List[str]) -> bool:` in `Auth` that returns `True` if the `path` is not in the list of strings `excluded_paths`:
- Returns `True` if `path` is `None`
- Returns `True` if `excluded_paths` is `None` or empty
- Returns `False` if `path` is in `excluded_paths`
- You can assume `excluded_paths` contains string path always ending by a `/`
- This method must be slash tolerant: `path=/api/v1/status` and `path=/api/v1/status/` must be returned `False` if `excluded_paths` contains `/api/v1/status/`
