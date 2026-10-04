from fastapi import FastAPI
from users import router as usersRouter
from tasks import router as tasksRouter

app = FastAPI()
app.include_router(usersRouter)
app.include_router(tasksRouter)