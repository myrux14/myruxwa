# core/config.py
from pathlib import Path
import os
from dotenv import load_dotenv

# -----------------------------
# CARGAR VARIABLES DE ENTORNO
# -----------------------------
load_dotenv()

ENV = os.getenv("ENV", "local")

# -----------------------------
# BASE DEL PROYECTO
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# DATABASE CONFIG
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# detectar tipo automáticamente
if DATABASE_URL and DATABASE_URL.startswith("postgres"):
    DB_TYPE = "postgres"
else:
    DB_TYPE = "sqlite"

# fallback local
DB_PATH = BASE_DIR / "data" / "app.db"

# crear carpeta si no existe (solo sqlite)
if DB_TYPE == "sqlite":
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# validación en producción
if DB_TYPE == "postgres" and not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida para PostgreSQL")

# -----------------------------
# APP
# -----------------------------
APP_NAME = "Water Analytics"
APP_VERSION = "1.0.0"

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
# DEBUG
# -----------------------------
DEBUG = ENV == "local"