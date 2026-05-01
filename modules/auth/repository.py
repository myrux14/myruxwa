# modules/auth/repository.py
from core.database import get_connection
from core.db_utils import p


def row_to_dict(cursor, row):
    if not row:
        return None
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row))


def get_user(username, password):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = f"""
            SELECT id, username, password, role, active, company_id
            FROM users
            WHERE username = {p()} AND password = {p()}
        """

        cursor.execute(query, (username, password))

        row = cursor.fetchone()
        return row_to_dict(cursor, row)

    except Exception as e:
        print("Error get_user:", e)
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()