from core.config import DB_TYPE


# -----------------------------
# PLACEHOLDER SQL
# -----------------------------
def p():
    """
    Devuelve el placeholder correcto según el motor.
    """
    return "%s" if DB_TYPE == "postgres" else "?"


# -----------------------------
# ROW → DICT
# -----------------------------
def row_to_dict(cursor, row):
    """
    Convierte una fila SQL en diccionario.
    """
    return {
        col[0]: row[idx]
        for idx, col in enumerate(cursor.description)
    }