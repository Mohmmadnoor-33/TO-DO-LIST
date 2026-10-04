from pydantic import BaseModel

class login(BaseModel):
    username: str
    password: str


class Task(BaseModel):
    task: str
    done: bool = False

