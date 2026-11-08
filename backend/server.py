import sqlite3
from pathlib import Path
from fastapi import FastAPI, HTTPException


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
