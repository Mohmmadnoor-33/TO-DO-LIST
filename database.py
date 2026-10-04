import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def get_connection():
    connection = psycopg2.connect(
        dbname="to_do_list",
        host="localhost",
        port="5432",
        user="postgres",
        password="MnMa2003"
    )
    return connection


