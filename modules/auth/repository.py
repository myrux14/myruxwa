# modules/auth/repository.py
from core.database import get_connection


def row_to_dict(cursor, row):
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row)) if row else None


def get_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, password, role, active, company_id
        FROM users
        WHERE username = %s AND password = %s
    """, (username, password))

    row = cursor.fetchone()
    user = row_to_dict(cursor, row)

    cursor.close()
    conn.close()

    return user