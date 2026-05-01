from core.config import DB_TYPE

def p():
    """
    Devuelve el placeholder correcto según el motor de base de datos.
    """
    return "%s" if DB_TYPE == "postgres" else "?"