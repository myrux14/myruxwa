from core.database import get_connection
from core.db_utils import p

# -----------------------------
# HELPER (CLAVE)
# -----------------------------
def row_to_dict(cursor, row):
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row)) if row else None


# -----------------------------
# GET ASSETS POR SITE
# -----------------------------
def get_assets_by_site(site_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * FROM assets
        WHERE site_id = {p()}
    """, (site_id,))

    rows = cursor.fetchall()
    result = [row_to_dict(cursor, row) for row in rows]

    cursor.close()
    conn.close()

    return result


# -----------------------------
# CREAR ASSET
# -----------------------------
def create_asset(name, type, site_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        INSERT INTO assets (name, type, site_id)
        VALUES ({p()}, {p()}, {p()})
    """, (name, type, site_id))

    conn.commit()

    cursor.close()
    conn.close()


# -----------------------------
# GET ASSET POR ID
# -----------------------------
def get_asset_by_id(asset_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM assets WHERE id = %s
    """, (asset_id,))

    row = cursor.fetchone()
    result = row_to_dict(cursor, row)

    cursor.close()
    conn.close()

    return result