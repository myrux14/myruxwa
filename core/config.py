# core/config.py
from pathlib import Path
import os
from dotenv import load_dotenv

# -----------------------------
# CARGAR VARIABLES DE ENTORNO
# -----------------------------
load_dotenv()

ENV = os.getenv("ENV", "local")
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida")

# -----------------------------
# BASE DEL PROYECTO
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# APP
# -----------------------------
APP_NAME = "Water Analytics"
APP_VERSION = "1.0.0"

# -----------------------------
# DATABASE (solo fallback local)
# -----------------------------
DB_PATH = BASE_DIR / "data" / "app.db"

# -----------------------------
# SEGURIDAD
# -----------------------------
SESSION_TIMEOUT_MINUTES = 60

# -----------------------------
# PARÁMETROS DE NEGOCIO (RSI)
# -----------------------------
RSI_IDEAL_MIN = 6.5
RSI_IDEAL_MAX = 7.5

RSI_MUYINCRUSTANTE = 6.0
RSI_MUYCORROSIVO = 8.5

# -----------------------------
# DEBUG (solo en local)
# -----------------------------
DEBUG = ENV == "local"