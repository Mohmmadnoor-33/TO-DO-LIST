# TO DO LIST PROJECT

A task management REST API where multiple users can sign up,
log in, and manage their own daily tasks, marking each one as done or pending.
Each user can only see and edit their own tasks.

## Features

- User registration and login with JWT authentication
- Passwords hashed with bcrypt
- Create, view, update, and delete your own tasks
- Filter tasks by status (done / pending)
- Pagination support

## Tech Stack

- Python, FastAPI
- PostgreSQL
- JWT, bcrypt

## Getting Started

1. Clone the repository:
   git clone https://github.com/Mohmmadnoor-33/TO-DO-LIST.git
   cd TO-DO-LIST

2. Create and activate a virtual environment, then install the dependencies:
   pip install -r requirements.txt

3. Create a `.env` file in the project folder and add your secret key:
   SECRET_KEY=your_secret_key_here

4. Create the PostgreSQL database `to_do_list` with the `users` and `tasks` tables.

5. Run the server:
   python -m uvicorn main:app --reload

6. Open the interactive docs at http://127.0.0.1:8000/docs

## API Endpoints

- POST /signup - register a new user
- POST /login - log in and receive a token
- POST /tasks - add a task
- GET /tasks - list your tasks (supports status, limit, offset)
- PUT /tasks/{id} - update a task
- DELETE /tasks/{id} - delete a task