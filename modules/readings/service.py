import pandas as pd
from modules.readings.repository import (
    create_reading,
    get_readings_by_asset,
    delete_readings_by_asset
)


# -----------------------------
# CRUD BÁSICO
# -----------------------------
def add_reading(asset_id, data):
    if not asset_id:
        return None

    create_reading(asset_id, data)
    return True


def list_readings(asset_id):
    return get_readings_by_asset(asset_id)


def clear_readings(asset_id):
    delete_readings_by_asset(asset_id)


# -----------------------------
# HELPERS
# -----------------------------
def safe_float(value):
    try:
        if pd.isna(value) or str(value).strip() == "":
            return None

        # soporta "1,234" o "7,5"
        value = str(value).replace(",", ".")
        return float(value)
    except:
        return None


def safe_date(value):
    try:
        d = pd.to_datetime(value, errors="coerce")
        if pd.isna(d):
            return None
        return str(d.date())
    except:
        return None


# -----------------------------
# CARGA DESDE EXCEL (ROBUSTA)
# -----------------------------
def load_readings_from_excel(asset_id, file):

    if not asset_id:
        return False, "Asset inválido"

    try:
        df = pd.read_excel(file)
    except Exception as e:
        return False, f"Error leyendo archivo: {e}"

    if df.empty:
        return False, "El archivo está vacío"

    # normalizar columnas
    df.columns = df.columns.str.strip().str.lower()

    column_map = {
        "date": ["date", "fecha"],
        "ph": ["ph"],
        "temperature": ["temperature", "temp", "temperatura", "temperature_c"],
        "tds": ["tds", "tds_ppm"],
        "calcium": ["calcium", "calcio", "calcium_hardness"],
        "alkalinity": ["alkalinity", "alcalinidad"]
    }

    def find_column(options):
        for opt in options:
            if opt in df.columns:
                return opt
        return None

    # mapear columnas
    mapped = {}
    for key, options in column_map.items():
        col = find_column(options)
        if not col:
            return False, f"Falta columna: {key}"
        mapped[key] = col

    insertados = 0
    errores = 0

    for i, row in df.iterrows():
        try:
            fecha = safe_date(row[mapped["date"]])

            # ❌ si no hay fecha → no insertamos
            if not fecha:
                raise ValueError("Fecha inválida")

            data = {
                "date": fecha,
                "ph": safe_float(row[mapped["ph"]]),
                "temperature": safe_float(row[mapped["temperature"]]),
                "tds": safe_float(row[mapped["tds"]]),
                "calcium": safe_float(row[mapped["calcium"]]),
                "alkalinity": safe_float(row[mapped["alkalinity"]])
            }

            create_reading(asset_id, data)
            insertados += 1

        except Exception as e:
            errores += 1
            print(f"[Fila {i}] Error: {e}")
            print("→ Data:", row.to_dict())

    return True, f"Carga completada: {insertados} registros, {errores} errores"