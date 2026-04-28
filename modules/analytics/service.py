import math


def calcular_lsi(ph, temperature_c, tds_ppm, calcium_hardness, alkalinity):
    try:
        # Factores
        A = (math.log10(tds_ppm) - 1) / 10
        B = -13.12 * math.log10(temperature_c + 273) + 34.55
        C = math.log10(calcium_hardness) - 0.4
        D = math.log10(alkalinity)

        pHs = (9.3 + A + B) - (C + D)

        lsi = ph - pHs

        return round(lsi, 2)
    except:
        return None


def clasificar_lsi(lsi):
    if lsi is None:
        return "Sin datos"
    elif lsi < -0.5:
        return "Muy Corrosiva"
    elif -0.5 <= lsi <= 0.5:
        return "ideal"
    else:
        return "Muy Incrustante"


def recomendaciones_lsi(row):
    lsi = row["LSI"]
    ph = row["ph"]
    alkalinity = row["alkalinity"]
    calcium = row["calcium"]

    if lsi is None:
        return "Sin datos"

    # -----------------------------
    # INCRUSTANTE
    # -----------------------------
    if lsi > 0.5:
        acciones = []

        if ph > 7.5:
            acciones.append("↓ Reducir pH")

        if alkalinity > 120:
            acciones.append("↓ Reducir alcalinidad")

        if calcium > 200:
            acciones.append("↓ Reducir calcio")

        if not acciones:
            acciones.append("Control general de incrustación")

        return " | ".join(acciones)

    # -----------------------------
    # CORROSIVO
    # -----------------------------
    elif lsi < -0.5:
        acciones = []

        if ph < 7.0:
            acciones.append("↑ Aumentar pH")

        if alkalinity < 100:
            acciones.append("↑ Aumentar alcalinidad")

        if not acciones:
            acciones.append("Control de corrosión")

        return " | ".join(acciones)

    # -----------------------------
    # ESTABLE
    # -----------------------------
    else:
        return "Sistema en equilibrio"

import numpy as np

def tendencia_lsi(df):
    if df is None or len(df) < 3:
        return "Sin datos suficientes", None

    df = df.sort_values("date")

    # convertir fechas a números
    x = np.arange(len(df))
    y = df["LSI"].values

    # regresión lineal
    slope, intercept = np.polyfit(x, y, 1)

    # clasificación
    if slope > 0.5:
        estado = "Subiendo (hacia incrustación)"
    elif slope < -0.5:
        estado = "Bajando (hacia corrosión)"
    else:
        estado = "Ideal"

    return estado, slope

def proyectar_lsi(df, pasos=3):
    if len(df) < 3:
        return None

    df = df.sort_values("date")

    x = np.arange(len(df))
    y = df["LSI"].values

    slope, intercept = np.polyfit(x, y, 1)

    futuros = []
    for i in range(1, pasos + 1):
        x_future = len(df) + i
        y_future = slope * x_future + intercept
        futuros.append(y_future)

    return futuros

import math

def calcular_componentes(row):
    try:
        tds = row["tds"]
        temp = row["temperature"]
        calcium = row["calcium"]
        alkalinity = row["alkalinity"]

        A = (math.log10(tds) - 1) / 10
        B = -13.12 * math.log10(temp + 273) + 34.55
        C = math.log10(calcium) - 0.4
        D = math.log10(alkalinity)

        return A, B, C, D
    except:
        return None, None, None, None