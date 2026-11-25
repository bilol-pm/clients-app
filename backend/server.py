import sqlite3
from pathlib import Path
from fastapi import FastAPI, HTTPException
import datetime
from pydantic import BaseModel, Field


DB_PATH = Path(__file__).parent / "clients.db"
app = FastAPI()

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        phone TEXT NOT NULL
    )    
    """)
    conn.commit()
    conn.close()    
init_db()

class ClientCreate(BaseModel):
    client_name: str = Field(min_length=1)
    date: datetime.date
    time: datetime.time
    phone: str = Field(pattern=r"^\+?[0-9 ]{7,15}$")

class ClientUpdate(BaseModel):
    client_name: str = Field(min_length=1)
    date: datetime.date
    time: datetime.time
    phone: str = Field(pattern=r"^\+?[0-9 ]{7,15}$")

@app.get("/clients")
def get_clients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients ORDER BY date, time")
    clients = cur.fetchall()
    conn.close()
    return [dict(client) for client in clients]

@app.post("/clients", status_code=201)
def create_client(client: ClientCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO clients (client_name, date, time, phone) VALUES (?, ?, ?, ?)",
        (client.client_name, client.date.isoformat(), client.time.strftime("%H:%M"), client.phone))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, "client_name": client.client_name, "date": client.date.isoformat(), "time": client.time.strftime("%H:%M"), "phone": client.phone}

@app.put("/clients/{client_id}")
def update_client(client_id: int, client: ClientUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    existing_client = cur.fetchall()
    if not existing_client:
        conn.close()
        raise HTTPException(status_code=404, detail="Client not found")
    cur.execute("UPDATE clients SET client_name = ?, date = ?, time = ?, phone = ? WHERE id = ?",
       (client.client_name, client.date.isoformat(), client.time.strftime("%H:%M"), client.phone, client_id))
    conn.commit()
    conn.close()
    return {"id": client_id, "client_name": client.client_name, "date": client.date.isoformat(), "time": client.time.strftime("%H:%M"), "phone": client.phone}

@app.delete("/clients/{client_id}")
def delete_client(client_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    deleted_count = cur.rowcount
    conn.close()
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"deleted": client_id}

    