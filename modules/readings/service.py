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
# CARGA DESDE EXCEL (ROBUSTA)
# -----------------------------
def load_readings_from_excel(asset_id, file):

    df = pd.read_excel(file)

    # limpiar columnas
    df.columns = df.columns.str.strip().str.lower()

    # 🔥 MAPEO FLEXIBLE REAL
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

    # -----------------------------
    # INSERTAR DATOS
    # -----------------------------
    for _, row in df.iterrows():
        try:
            data = {
                "date": str(pd.to_datetime(row[mapped["date"]]).date()),
                "ph": float(row[mapped["ph"]]),
                "temperature": float(row[mapped["temperature"]]),
                "tds": float(row[mapped["tds"]]),
                "calcium": float(row[mapped["calcium"]]),
                "alkalinity": float(row[mapped["alkalinity"]])
            }

            create_reading(asset_id, data)

        except Exception as e:
            return False, f"Error en fila: {e}"

    return True, "Datos cargados correctamente"

from modules.readings.repository import delete_readings_by_asset

def clear_readings(asset_id):
    delete_readings_by_asset(asset_id)

