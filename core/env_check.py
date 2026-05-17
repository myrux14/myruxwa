from core.database import get_db_info
from core.config import ENV


def check_environment():

    info = get_db_info()

    # ======================================
    # ALERTAS
    # ======================================
    alerts = []

    # producción usando local
    if (

        ENV == "production"
        and "localhost" in info["host"]

    ):

        alerts.append(
            (
                "error",
                "⚠️ Producción usando DB local"
            )
        )

    # local usando prod
    if (

        ENV == "local"
        and "render" in info["host"]

    ):

        alerts.append(
            (
                "warning",
                "⚠️ Estás usando DB producción"
            )
        )

    return {

        "env": ENV,
        "db": info["db"],
        "host": info["host"],
        "user": info["user"],
        "alerts": alerts
    }