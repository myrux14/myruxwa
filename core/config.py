# core/config.py

from pathlib import Path

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
# DATABASE
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
# DEBUG
# -----------------------------
DEBUG = True