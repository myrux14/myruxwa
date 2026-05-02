# modules/auth/repository.py
from core.database import get_connection
from core.db_utils import p
from core.security import hash_password, verify_password


def row_to_dict(cursor, row):
    if not row:
        return None
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row))

# -----------------------------
# LOGIN
# -----------------------------
def get_user(username, password):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT id, username, password, role, active, company_id
            FROM users
            WHERE username = {p()}
        """, (username,))

        row = cursor.fetchone()

        if not row:
            return None

        user = row_to_dict(cursor, row)

        # 🔐 VALIDACIÓN BCRYPT
        if not verify_password(password, user["password"]):
            return None

        return user

    except Exception as e:
        print("Error get_user:", e)
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -----------------------------
# CREAR
# -----------------------------
def create_user(username, password, role, company_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"SELECT id FROM users WHERE username = {p()}",
            (username,)
        )

        # validar duplicado
        if cursor.fetchone():
            return False, "Usuario ya existe"

        # 🔐 HASH PASSWORD
        hashed_password = hash_password(password)

        # insertar usuario
        cursor.execute(f"""
            INSERT INTO users (username, password, role, active, company_id)
            VALUES ({p()}, {p()}, {p()}, {p()}, {p()})
        """, (username, hashed_password, role, 1, company_id))
        
        conn.commit()
        return True, "Usuario creado"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cursor.close()
        conn.close()

# -----------------------------
# LISTAR
# -----------------------------
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, role, active, company_id
        FROM users
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    users = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return users

# -----------------------------
# ACTUALIZAR
# -----------------------------
def update_user(user_id, role, company_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            UPDATE users
            SET role = {p()}, company_id = {p()}
            WHERE id = {p()}
        """, (role, company_id, user_id))

        conn.commit()
        return True, "Usuario actualizado"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cursor.close()
        conn.close()

# -----------------------------
# ACTIVAR / DESACTIVAR
# -----------------------------
def toggle_user(user_id, active):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            UPDATE users
            SET active = {p()}
            WHERE id = {p()}
        """, (active, user_id))

        conn.commit()
        return True, "Estado actualizado"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cursor.close()
        conn.close()


# -----------------------------
# ELIMINAR
# -----------------------------
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"DELETE FROM users WHERE id = {p()}",
            (user_id,)
        )

        conn.commit()
        return True, "Usuario eliminado"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cursor.close()
        conn.close()

def reset_password(user_id, new_password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        hashed = hash_password(new_password)

        cursor.execute(f"""
            UPDATE users
            SET password = {p()}
            WHERE id = {p()}
        """, (hashed, user_id))

        conn.commit()
        return True, "Contraseña actualizada"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cursor.close()
        conn.close()