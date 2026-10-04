from model import Task
from fastapi import APIRouter ,HTTPException ,Depends
from users import get_current_user
import psycopg2.extras
from database import get_connection
from typing import Optional

router = APIRouter()

@router.post("/enter_tasks")
def create_task(task: Task, user_id : int  = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("INSERT INTO tasks (user_id,task,done) VALUES (%s,%s,%s)" , (user_id,task.task,task.done))
    connection.commit()
    connection.close()
    return {"status": "success"}

@router.get("/tasks")
def get_tasks(user_id: int = Depends(get_current_user), limit: int = 10, offset: int = 0, status: Optional[str] = None):
    if status is not None and status not in ("done", "pending"):
        raise HTTPException(status_code=400, detail="status must be done or pending")

    connection = get_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if status is None:
        cursor.execute("SELECT * FROM tasks WHERE user_id = %s LIMIT %s OFFSET %s",
                       (user_id, limit, offset))
    else:
        done_value = (status == "done")
        cursor.execute("SELECT * FROM tasks WHERE user_id = %s AND done = %s LIMIT %s OFFSET %s",
                       (user_id, done_value, limit, offset))

    tasks = cursor.fetchall()
    connection.close()
    return tasks

@router.put("/tasks/{id_mission}")
def update_task(id_mission : int, user_id : int = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("UPDATE tasks SET done = TRUE WHERE user_id = %s AND id = %s" , (user_id,id_mission))
    if cursor.rowcount > 0:
      connection.commit()
      connection.close()
      return {"status": "update_success"}
    else:
        connection.close()
        raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{id_mission}")
def delete_task(id_mission : int , user_id : int = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("DELETE FROM tasks WHERE user_id = %s AND id = %s"  , (user_id,id_mission))
    if cursor.rowcount > 0:
       connection.commit()
       connection.close()
       return {"status": "delete success"}
    else:
        connection.close()
        raise HTTPException(status_code=404, detail="Task not found")
    #task