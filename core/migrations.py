from core.database import get_connection
from core.config import DB_TYPE
from core.db_utils import p


def run_migrations():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # -----------------------------
        # ID dinámico
        # -----------------------------
        id_type = "SERIAL PRIMARY KEY" if DB_TYPE == "postgres" else "INTEGER PRIMARY KEY AUTOINCREMENT"

        # -----------------------------
        # TABLA MIGRATIONS
        # -----------------------------
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS migrations (
            id {id_type},
            name TEXT UNIQUE
        )
        """)

        # -----------------------------
        # MIGRACIÓN 001 - READINGS
        # -----------------------------
        if not migration_applied(cursor, "001_create_readings"):

            date_type = "DATE" if DB_TYPE == "postgres" else "TEXT"

            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS readings (
                id {id_type},
                asset_id INTEGER,
                date {date_type},
                ph REAL,
                temperature REAL,
                tds REAL,
                calcium REAL,
                alkalinity REAL
            )
            """)

            mark_migration(cursor, "001_create_readings")

        conn.commit()

    except Exception as e:
        print("Error en migraciones:", e)
        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# -----------------------------
# HELPERS
# -----------------------------
def migration_applied(cursor, name):
    cursor.execute(
        f"SELECT 1 FROM migrations WHERE name = {p()}",
        (name,)
    )
    return cursor.fetchone() is not None


def mark_migration(cursor, name):
    cursor.execute(
        f"INSERT INTO migrations (name) VALUES ({p()})",
        (name,)
    )