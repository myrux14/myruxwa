# core/database.py
import psycopg2
from core.config import DATABASE_URL


# -----------------------------
# CONEXIÓN
# -----------------------------
def get_connection():
    return psycopg2.connect(DATABASE_URL)


# -----------------------------
# INICIALIZAR BASE DE DATOS
# -----------------------------
def init_db():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # -----------------------------
        # TABLAS
        # -----------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            active INTEGER,
            company_id INTEGER REFERENCES companies(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sites (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            company_id INTEGER REFERENCES companies(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            site_id INTEGER REFERENCES sites(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id SERIAL PRIMARY KEY,
            asset_id INTEGER REFERENCES assets(id),
            date DATE,
            ph REAL,
            temperature REAL,
            tds REAL,
            calcium REAL,
            alkalinity REAL
        )
        """)

        # -----------------------------
        # COMPANY DEFAULT
        # -----------------------------
        cursor.execute("""
        INSERT INTO companies (id, name)
        VALUES (1, 'Default Company')
        ON CONFLICT (id) DO NOTHING
        """)

        # -----------------------------
        # ADMIN USER
        # -----------------------------
        cursor.execute(
            "SELECT id FROM users WHERE username = %s",
            ("admin",)
        )
        existing_user = cursor.fetchone()

        if not existing_user:
            cursor.execute("""
                INSERT INTO users (username, password, role, active, company_id)
                VALUES (%s, %s, %s, %s, %s)
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