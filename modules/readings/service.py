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
# CARGA DESDE EXCEL (MEJORADA)
# -----------------------------
def load_readings_from_excel(asset_id, file):

    df = pd.read_excel(file)
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

    mapped = {}
    for key, options in column_map.items():
        col = find_column(options)
        if not col:
            return False, f"Falta columna: {key}"
        mapped[key] = col

    errores = 0
    insertados = 0

    for i, row in df.iterrows():
        try:
            # manejar NaN
            if pd.isna(row[mapped["ph"]]):
                continue

            data = {
                "date": str(pd.to_datetime(row[mapped["date"]]).date()),
                "ph": float(row[mapped["ph"]]),
                "temperature": float(row[mapped["temperature"]]),
                "tds": float(row[mapped["tds"]]),
                "calcium": float(row[mapped["calcium"]]),
                "alkalinity": float(row[mapped["alkalinity"]])
            }

            create_reading(asset_id, data)
            insertados += 1

        except Exception as e:
            errores += 1
            continue  # 🔥 no detener todo el proceso

    return True, f"Carga completada: {insertados} registros, {errores} errores"

