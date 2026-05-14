from core.lsi_table import calcular_lsi

RANGO_ESTABLE_MIN = -0.3
RANGO_ESTABLE_MAX = 0.3


def ajustar_parametros(row):

    ph = row["ph"]
    temp = row["temperature"]
    tds = row["tds"]
    calcium = row["calcium"]
    alkalinity = row["alkalinity"]

    lsi = calcular_lsi(
        ph,
        temp,
        tds,
        calcium,
        alkalinity
    )

    if lsi is None:
        return None
    # guardar originales
    original = {
        "ph": ph,
        "temperature": temp,
        "tds": tds,
        "calcium": calcium,
        "alkalinity": alkalinity,
        "LSI_original": lsi
    }

    # -----------------------------
    # INCRUSTACIÓN
    # -----------------------------
    if lsi > RANGO_ESTABLE_MAX:

        while lsi > 0.3:

            if ph > 7.0:
                ph -= 0.05

            elif alkalinity > 80:
                alkalinity -= 5

            elif calcium > 100:
                calcium -= 5

            else:
                break

            lsi = calcular_lsi(
                ph,
                tds,
                temp,
                calcium,
                alkalinity
            )

    # -----------------------------
    # CORROSIÓN
    # -----------------------------
    elif lsi < RANGO_ESTABLE_MIN:

        while lsi < -0.3:

            if ph < 8.2:
                ph += 0.05

            elif alkalinity < 120:
                alkalinity += 5

            else:
                break

            lsi = calcular_lsi(
                ph,
                tds,
                temp,
                calcium,
                alkalinity
            )

    return {
        **original,
        "ph_ajustado": round(ph, 2),
        "alkalinity_ajustada": round(alkalinity, 2),
        "calcium_ajustado": round(calcium, 2),
        "LSI_ajustado": round(lsi, 2)
    }