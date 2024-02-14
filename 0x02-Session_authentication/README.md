# Simple API

Simple HTTP API for playing with `User` model.


## Files

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


## Setup

```
$ pip3 install -r requirements.txt
```


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)

# Session Authentication

## Tasks

### Task 0
Building on the work from [0x06. Basic authentication](../0x06-Basic_authentication), add a new endpoint: `GET /users/me` to retrieve the authenticated `User` object.
- Copy folders `models` and `api` from the previous project.
- Update `@app.before_request` in `api/v1/app.py`:
	- Assign the result of `auth.current_user(request)` to `request.current_user`
- Update method for the route `GET /api/v1/users/<user_id>` in `api/v1/views/users.py`:
	- If `<user_id>` is equal to `me` and `request.current_user` is `None`: `abort(404)`
	- If `<user_id>` is equal to `me` and `request.current_user` is not `None`: return the authenticated `User` in a JSON response (like a normal case of `GET /api/v1/users/<user_id>` where `<user_id>` is a valid `User` ID)
	- Otherwise, keep the same behavior

### Task 1
Create a class `SessionAuth` that inherits from `Auth`. For the moment this class will be empty. It’s the first step for creating a new authentication mechanism.

Update `api/v1/app.py` for using `SessionAuth` instance for the variable `auth` depending of the value of the environment variable `AUTH_TYPE`, If `AUTH_TYPE` is equal to `session_auth`:
- import `SessionAuth` from `api.v1.auth.session_auth`
- create an instance of S`essionAuth` and assign it to the variable `auth`

Otherwise, keep the previous mechanism.

### Task 2
Update `SessionAuth` class:
- Create a class attribute `user_id_by_session_id` initialized by an empty dictionary
- Create an instance method `def create_session(self, user_id: str = None) -> str:` that creates a Session ID for a `user_id`:
	- Return `None` if `user_id` is `None`
	- Return `None` if `user_id` is not a string
	- Otherwise:
		- Generate a Session ID using `uuid` module and `uuid4()`
		- Use this Session ID as key of the dictionary `user_id_by_session_id` - the value for this key must be `user_id`
		- Return the Session ID
	- The same `user_id` can have multiple Session ID - the `user_id` is the value in the dictionary `user_id_by_session_id`

### Task 3
Update `SessionAuth` class:
Create an instance method `def user_id_for_session_id(self, session_id: str = None) -> str:` that returns a `User` ID based on a Session ID:
- Return `None` if `session_id` is `None`
- Return `None` if `session_id` is not a string
- Return the value (the User ID) for the key `session_id` in the dictionary `user_id_by_session_id`.
- You must use `.get()` built-in for accessing in a dictionary a value based on key

### Task 4
Update `api/v1/auth/auth.py` by adding the method `def session_cookie(self, request=None):` that returns a cookie value from a request:
- Return `None` if `request` is `None`
- Return the value of the cookie named `_my_session_id` from request - the name of the cookie must be defined by the environment variable `SESSION_NAME`
- You must use `.get()` to access the cookie in the request cookies dictionary
- You must use the environment variable `SESSION_NAME` to define the name of the cookie used for the Session ID

### Task 5
Update the `@app.before_request` method in `api/v1/app.py`:
- Add the URL path `/api/v1/auth_session/login/` in the list of excluded paths of the method `require_auth` - this route doesn’t exist yet but it should be accessible outside authentication
- If `auth.authorization_header(request)` and `auth.session_cookie(request)` return `None`, `abort(401)`

### Task 6
Update `SessionAuth` class:
Create an instance method `def current_user(self, request=None):` (overload) that returns a `User` instance based on a cookie value:
- You must use `self.session_cookie(...)` and `self.user_id_for_session_id(...)` to return the User ID based on the cookie `_my_session_id`
- By using this User ID, you will be able to retrieve a `User` instance from the database - you can use `User.get(...)` for retrieving a `User` from the database.

### Task 7
Create a new Flask view that handles all routes for the Session authentication.

In the file `api/v1/views/session_auth.py`, create a route `POST /auth_session/login`:
- Slash tolerant (`/auth_session/login` == `/auth_session/login/`)
- You must use `request.form.get()` to retrieve `email` and `password` parameters
- If `email` is missing or empty, return the JSON `{ "error": "email missing" }` with the status code `400`
- If `password` is missing or empty, return the JSON `{ "error": "password missing" }` with the status code `400`
- Retrieve the `User` instance based on the `email` - you must use the class method `search` of `User`
	- If no `User` found, return the JSON `{ "error": "no user found for this email" }` with the status code `404`
	- If the `password` is not the one of the `User` found, return the JSON `{ "error": "wrong password" }` with the status code `401` - you must use `is_valid_password` from the `User` instance
	- Otherwise, create a Session ID for the `User` ID:
		- You must use from `api.v1.app import auth` - WARNING: please import it only where you need it - not on top of the file (can generate circular import - and break first tasks of this project)
		- You must use `auth.create_session(..)` for creating a Session ID
		- Return the dictionary representation of the `User` - you must use `to_json()` method from `User`
		- You must set the cookie to the response - you must use the value of the environment variable `SESSION_NAME` as cookie name

In the file `api/v1/views/__init__.py`, you must add this new view.

### Task 8
Update the class `SessionAuth` by adding a new method `def destroy_session(self, request=None):` that deletes the user session / logout:
- If the `request` is equal to `None`, return `False`
- If the `request` doesn’t contain the Session ID cookie, return `False` - you must use `self.session_cookie(request)`
- If the Session ID of the request is not linked to any User ID, return `False` - you must use `self.user_id_for_session_id(...)`
- Otherwise, delete in `self.user_id_by_session_id` the Session ID (as key of this dictionary) and return `True`

Update the file `api/v1/views/session_auth.py`, by adding a new route `DELETE /api/v1/auth_session/logout`:
- Slash tolerant
- You must use `from api.v1.app import auth`
- You must use `auth.destroy_session(request)` for deleting the Session ID contains in the request as cookie:
	- If `destroy_session` returns `False`, `abort(404)`
	- Otherwise, return an empty JSON dictionary with the status code 200
