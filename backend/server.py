import sqlite3
from pathlib import Path
from fastapi import FastAPI
import datetime
from typing import Literal
from pydantic import BaseModel, Field, EmailStr

DB_PATH = Path(__file__).parent / "barber.db"
app = FastAPI()
SERVICES = {"haircut": 30, "haircut_beard": 45}

class BookingCreate(BaseModel):
    client_name: str = Field(min_length=1)
    email: EmailStr
    phone: str = Field(pattern=r"^\+?[0-9 ]{7,15}$")
    service: Literal["haircut", "haircut_beard"]
    date: datetime.date
    start_time: datetime.time

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

@app.post("/bookings", status_code=201)
def create_booking(booking: BookingCreate):
    end_time = calculate_end_time(booking.date, booking.start_time, booking.service)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO bookings (client_name, email, phone, service, date, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (booking.client_name, booking.email, booking.phone, booking.service, booking.date, booking.start_time, end_time),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, "end_time": end_time}


