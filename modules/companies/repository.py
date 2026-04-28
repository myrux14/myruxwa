from core.database import get_connection


def get_companies():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM companies")
    rows = cursor.fetchall()
    conn.close()

    return [dict(zip(row.keys(), row)) for row in rows]


def get_company_by_id(company_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM companies WHERE id = ?
    """, (company_id,))

    row = cursor.fetchone()
    conn.close()

    return dict(zip(row.keys(), row)) if row else None


def create_company(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO companies (name) VALUES (?)
    """, (name,))

    conn.commit()
    conn.close()