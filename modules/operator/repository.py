from core.database import get_connection
from core.db_utils import p


def get_company_dashboard_data(
    company_id
):

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT

                c.name as company_name,

                s.id as system_id,
                s.name as system_name,
                s.chemistry_model,

                a.name as asset_type

            FROM companies c

            LEFT JOIN systems s
                ON s.company_id = c.id

            LEFT JOIN asset_types a
                ON a.id = s.asset_type_id

            WHERE c.id = {p()}
            """,
            (company_id,)
        )

        rows = cursor.fetchall()

        columns = [
            desc[0]
            for desc in cursor.description
        ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    except Exception as e:

        print(e)
        return []

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()