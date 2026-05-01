from core.database import get_connection

def run_migrations():
    conn = get_connection()
    cursor = conn.cursor()

    # tabla de control
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS migrations (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE
    )
    """)

    # -----------------------------
    # MIGRACIÓN 001
    # -----------------------------
    if not migration_applied(cursor, "001_create_readings"):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id SERIAL PRIMARY KEY,
            asset_id INTEGER,
            date TEXT,
            ph REAL,
            temperature REAL,
            tds REAL,
            calcium REAL,
            alkalinity REAL
        )
        """)
        mark_migration(cursor, "001_create_readings")

    conn.commit()
    conn.close()


def migration_applied(cursor, name):
    cursor.execute("SELECT 1 FROM migrations WHERE name = %s", (name,))
    return cursor.fetchone() is not None


def mark_migration(cursor, name):
    cursor.execute("INSERT INTO migrations (name) VALUES (%s)", (name,))