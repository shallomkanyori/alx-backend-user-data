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

### Task 5
Validate all requests to secure the API:

Update the method `def authorization_header(self, request=None) -> str:` in `api/v1/auth/auth.py`:
- If `request` is `None`, return `None`
- If `request` doesn’t contain the header key `Authorization`, return `None`
- Otherwise, return the value of the header request `Authorization`

Update the file `api/v1/app.py`:
- Create a variable `auth` initialized to `None` after the `CORS` definition
- Based on the environment variable `AUTH_TYPE`, load and assign the right instance of authentication to `auth`
	- if `auth`:
		- import `Auth` from `api.v1.auth.auth`
		- create an instance of `Auth` and assign it to the variable `auth`

Now the biggest piece is the filtering of each request. For that you will use the Flask method `before_request`
- Add a method in `api/v1/app.py` to handle `before_request`
	- if `auth` is `None`, do nothing
	- if `request.path` is not part of this list `['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']`, do nothing - you must use the method `require_auth` from the `auth` instance
	- if `auth.authorization_header(request)` returns `None`, raise the error `401` - you must use `abort`
	- if `auth.current_user(request)` returns `None`, raise the error `403` - you must use `abort`

### Task 6
Create a class `BasicAuth` that inherits from `Auth`. For the moment this class will be empty.

Update `api/v1/app.py` to use `BasicAuth` class instead of `Auth` depending of the value of the environment variable `AUTH_TYPE`. If `AUTH_TYPE` is equal to `basic_auth`:
- import `BasicAuth` from `api.v1.auth.basic_auth`
- create an instance of `BasicAuth` and assign it to the variable `auth`

Otherwise, keep the previous mechanism with `auth` as an instance of `Auth`.

### Task 7
Add the method `def extract_base64_authorization_header(self, authorization_header: str) -> str:` in the class `BasicAuth` that returns the Base64 part of the Authorization header for a Basic Authentication:
- Return `None` if `authorization_header` is `None`
- Return `None` if `authorization_header` is not a string
- Return `None` if `authorization_header` doesn’t start with `Basic` (with a space at the end)
- Otherwise, return the value after `Basic` (after the space)
- You can assume `authorization_header` contains only one `Basic`

### Task 8
Add the method `def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:` in the class `BasicAuth` that returns the decoded value of a Base64 string `base64_authorization_header`:
- Return `None` if `base64_authorization_header` is `None`
- Return `None` if `base64_authorization_header` is not a string
- Return `None` if `base64_authorization_header` is not a valid Base64 - you can use `try/except`
- Otherwise, return the decoded value as UTF8 string - you can use `decode('utf-8')`

### Task 9
Add the method `def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str)` in the class `BasicAuth` that returns the user email and password from the Base64 decoded value.
- This method must return 2 values
- Return `None, None` if `decoded_base64_authorization_header` is `None`
- Return `None, None` if `decoded_base64_authorization_header` is not a string
- Return `None, None` if `decoded_base64_authorization_header` doesn’t contain `:`
- Otherwise, return the user email and the user password - these 2 values must be separated by a `:`
- You can assume `decoded_base64_authorization_header` will contain only one `:`
