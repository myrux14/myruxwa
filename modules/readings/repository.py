from core.database import get_connection


# -----------------------------
# HELPER
# -----------------------------
def row_to_dict(cursor, row):
    columns = [desc[0] for desc in cursor.description]
    return dict(zip(columns, row)) if row else None


# -----------------------------
# CREATE READING
# -----------------------------
def create_reading(asset_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO readings (
            asset_id, date, ph, temperature, tds, calcium, alkalinity
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        asset_id,
        data["date"],
        data["ph"],
        data["temperature"],
        data["tds"],
        data["calcium"],
        data["alkalinity"]
    ))

    conn.commit()
    cursor.close()
    conn.close()


# -----------------------------
# GET READINGS BY ASSET
# -----------------------------
def get_readings_by_asset(asset_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM readings
        WHERE asset_id = %s
        ORDER BY date DESC
    """, (asset_id,))

    rows = cursor.fetchall()
    result = [row_to_dict(cursor, row) for row in rows]

    cursor.close()
    conn.close()

    return result


# -----------------------------
# DELETE READINGS
# -----------------------------
def delete_readings_by_asset(asset_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM readings WHERE asset_id = %s
    """, (asset_id,))

    conn.commit()
    cursor.close()
    conn.close()