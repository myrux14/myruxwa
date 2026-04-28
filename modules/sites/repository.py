from core.database import get_connection


def get_sites_by_company(company_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM sites
        WHERE company_id = ?
    """, (company_id,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(zip(row.keys(), row)) for row in rows]


def create_site(name, company_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sites (name, company_id)
        VALUES (?, ?)
    """, (name, company_id))

    conn.commit()
    conn.close()


def get_site_by_id(site_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM sites WHERE id = ?
    """, (site_id,))

    row = cursor.fetchone()
    conn.close()

    return dict(zip(row.keys(), row)) if row else None