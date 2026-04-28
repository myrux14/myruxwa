# core/database.py

import sqlite3
from core.config import DB_PATH
from pathlib import Path


# -----------------------------
# CONEXIÓN
# -----------------------------
# 📌 Ruta segura en Render
DB_PATH = Path("data/app.db")

# crear carpeta si no existe
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# -----------------------------
# INICIALIZAR BASE DE DATOS
# -----------------------------
def init_db():
    # 🔥 crear carpeta si no existe
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------
    # TABLA COMPANIES
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    # -----------------------------
    # TABLA USERS
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        active INTEGER,
        company_id INTEGER,
        FOREIGN KEY (company_id) REFERENCES companies(id)
    )
    """)

    # -----------------------------
    # TABLA SITES
    # -----------------------------
    # core/database.py

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        company_id INTEGER,
        FOREIGN KEY (company_id) REFERENCES companies(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT,
        site_id INTEGER,
        FOREIGN KEY (site_id) REFERENCES sites(id)
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_id INTEGER,
        date TEXT,
        ph REAL,
        temperature REAL,
        tds REAL,
        calcium REAL,
        alkalinity REAL,
        FOREIGN KEY (asset_id) REFERENCES assets(id)
    )
    """)


    conn.commit()
    conn.close()