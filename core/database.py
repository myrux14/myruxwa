# core/database.py

import sqlite3
from pathlib import Path

# -----------------------------
# RUTA DB (RENDER SAFE)
# -----------------------------
DB_PATH = Path("data/app.db")

# crear carpeta si no existe
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


# -----------------------------
# CONEXIÓN
# -----------------------------
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# -----------------------------
# INICIALIZAR BASE DE DATOS
# -----------------------------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

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

    # -----------------------------
    # CREAR COMPANY DEFAULT
    # -----------------------------
    cursor.execute("""
    INSERT OR IGNORE INTO companies (id, name)
    VALUES (1, 'Default Company')
    """)

    # -----------------------------
    # CREAR ADMIN SI NO EXISTE
    # -----------------------------
    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute("""
            INSERT INTO users (username, password, role, active, company_id)
            VALUES (?, ?, ?, ?, ?)
        """, ("admin", "admin123", "admin", 1, 1))

    conn.commit()
    conn.close()