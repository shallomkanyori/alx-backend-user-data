# User authentication service

## Tasks

### Task 0
Create a SQLAlchemy model named `User` for a database table named `users`.

The model will have the following attributes:
- `id`, the integer primary key
- `email`, a non-nullable string
- `hashed_password`, a non-nullable string
- `session_id`, a nullable string
- `reset_token`, a nullable string
