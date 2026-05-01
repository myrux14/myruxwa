# core/database.py
import psycopg2
import sqlite3
from core.config import DATABASE_URL, DB_TYPE, DB_PATH


# -----------------------------
# CONEXIÓN
# -----------------------------
def get_connection():
    if DB_TYPE == "postgres":
        return psycopg2.connect(DATABASE_URL)
    else:
        return sqlite3.connect(DB_PATH)


# -----------------------------
# CURSOR (HELPER)
# -----------------------------
def get_cursor(conn):
    if DB_TYPE == "postgres":
        return conn.cursor()
    else:
        return conn.cursor()


# -----------------------------
# INIT DB (SOLO BASE MÍNIMA)
# -----------------------------
def init_db():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # -----------------------------
        # TABLAS BASE (SOLO SI NO USAS MIGRACIONES)
        # -----------------------------
        if DB_TYPE == "postgres":
            id_type = "SERIAL PRIMARY KEY"
        else:
            id_type = "INTEGER PRIMARY KEY AUTOINCREMENT"

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS companies (
            id {id_type},
            name TEXT NOT NULL
        )
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS users (
            id {id_type},
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            active INTEGER,
            company_id INTEGER
        )
        """)

        # -----------------------------
        # DATA INICIAL
        # -----------------------------
        placeholder = "%s" if DB_TYPE == "postgres" else "?"

        # company default
        cursor.execute(f"""
        INSERT INTO companies (id, name)
        VALUES (1, 'Default Company')
        ON CONFLICT DO NOTHING
        """)

        # admin
        cursor.execute(
            f"SELECT id FROM users WHERE username = {placeholder}",
            ("admin",)
        )
        existing_user = cursor.fetchone()

        if not existing_user:
            cursor.execute(f"""
                INSERT INTO users (username, password, role, active, company_id)
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
            """, ("admin", "admin123", "admin", 1, 1))

        conn.commit()

    except Exception as e:
        print("Error inicializando DB:", e)
        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()