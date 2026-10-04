import psycopg2.extras
from database import get_connection ,SECRET_KEY
import bcrypt
from fastapi import APIRouter, HTTPException, Depends
from model import login
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import datetime

security = HTTPBearer()
router = APIRouter()
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.InvalidTokenError :
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/signup")
def sign_up(signup: login):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT username FROM users WHERE username = LOWER(%s)", (signup.username,))
    result = cursor.fetchone()
    if result is not None:
        connection.close()
        raise HTTPException(status_code=400, detail="username is already exist")
    #password_bytes = signup.password.encode()
    hashed = bcrypt.hashpw(signup.password.encode(), bcrypt.gensalt())
    hashed_str = hashed.decode()
    cursor.execute("INSERT INTO users (username , password) VALUES (%s, %s)", (signup.username, hashed_str))
    connection.commit()
    connection.close()
    return {"messages" : "success sign up"}


@router.post("/login")
def login(user_login: login):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT id,username, password FROM users WHERE username = LOWER(%s)", (user_login.username,))
    user = cursor.fetchone()

    if user is None:
        connection.close()
        raise HTTPException(status_code=401, detail="Invalid username or password")

    check_password = bcrypt.checkpw(user_login.password.encode(), user["password"].encode())

    if not check_password:
        connection.close()
        raise HTTPException(status_code=401, detail="Username or password is incorrect")

    connection.close()
    return {"message": "success login in", "access_token": jwt.encode({"user_id" :user["id"] , "exp" : datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours = 1)}
            , SECRET_KEY, algorithm="HS256")}


@router.get("/test_protected")
def test_protected(user_id: int = Depends(get_current_user)):
    return {"your_user_id": user_id}