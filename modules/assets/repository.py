from core.database import get_connection


def get_assets_by_site(site_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM assets
        WHERE site_id = ?
    """, (site_id,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(zip(row.keys(), row)) for row in rows]


def create_asset(name, type, site_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO assets (name, type, site_id)
        VALUES (?, ?, ?)
    """, (name, type, site_id))

    conn.commit()
    conn.close()


def get_asset_by_id(asset_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM assets WHERE id = ?
    """, (asset_id,))

    row = cursor.fetchone()
    conn.close()

    return dict(zip(row.keys(), row)) if row else None