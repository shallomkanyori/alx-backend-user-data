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
