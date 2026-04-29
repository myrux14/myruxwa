from core.database import get_connection


# -----------------------------
# HELPER
# -----------------------------
def row_to_dict(cursor, row):
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row)) if row else None


# -----------------------------
# GET SITES BY COMPANY
# -----------------------------
def get_sites_by_company(company_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM sites
        WHERE company_id = %s
    """, (company_id,))

    rows = cursor.fetchall()
    result = [row_to_dict(cursor, row) for row in rows]

    cursor.close()
    conn.close()

    return result


# -----------------------------
# CREATE SITE
# -----------------------------
def create_site(name, company_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sites (name, company_id)
        VALUES (%s, %s)
        RETURNING id
    """, (name, company_id))

    new_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return new_id


# -----------------------------
# GET SITE BY ID
# -----------------------------
def get_site_by_id(site_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM sites WHERE id = %s
    """, (site_id,))

    row = cursor.fetchone()
    result = row_to_dict(cursor, row)

    cursor.close()
    conn.close()

    return result