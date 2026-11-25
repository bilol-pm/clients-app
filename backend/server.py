import sqlite3
from pathlib import Path
from fastapi import FastAPI
import datetime

DB_PATH = Path(__file__).parent / "barber.db"
app = FastAPI()
SERVICES = {"haircut": 30, "haircut_beard": 45}

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        service TEXT NOT NULL,
        date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()

init_db()

def calculate_end_time(date, start_time, service):
    start = datetime.datetime.combine(date, start_time)
    end = start + datetime.timedelta(minutes=SERVICES.get(service, 30))
    return end.strftime("%H:%M")
