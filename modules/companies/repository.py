from core.database import get_connection


# -----------------------------
# HELPER
# -----------------------------
def row_to_dict(cursor, row):
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row)) if row else None


# -----------------------------
# GET ALL COMPANIES
# -----------------------------
def get_companies():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM companies")
    rows = cursor.fetchall()

    result = [row_to_dict(cursor, row) for row in rows]

    cursor.close()
    conn.close()

    return result


# -----------------------------
# GET COMPANY BY ID
# -----------------------------
def get_company_by_id(company_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM companies WHERE id = %s
    """, (company_id,))

    row = cursor.fetchone()
    result = row_to_dict(cursor, row)

    cursor.close()
    conn.close()

    return result


# -----------------------------
# CREATE COMPANY
# -----------------------------
def create_company(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO companies (name)
        VALUES (%s)
        RETURNING id
    """, (name,))

    new_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return new_id