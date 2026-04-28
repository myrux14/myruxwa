# modules/auth/repository.py

from core.database import get_connection

def get_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()

    return {k: user[k] for k in user.keys()} if user else None