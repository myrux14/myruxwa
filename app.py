import pandas as pd
import streamlit as st

from core.config import ENV, DATABASE_URL
import streamlit as st

st.sidebar.write("ENV:", ENV)
st.sidebar.write("DB:", DATABASE_URL[:50])

# 🔥 SIEMPRE PRIMERO
st.set_page_config(page_title="Water Analytics", layout="wide")

# ahora sí imports
from core.config import APP_NAME, ENV
from core.database import init_db
from modules.auth.ui import login

# UI ENV
st.sidebar.info(f"Entorno: {ENV}")

# init solo en local
if ENV == "local":
    init_db()

# ----------------------------- 
# # RESTAURAR SESIÓN DESDE URL 
# # ----------------------------- 
params = st.query_params 
if "token" in params: 
    st.session_state.logged_in = True 
    st.session_state.token = params.get("token") 
    st.session_state.user = params.get("user") 
    st.session_state.role = params.get("role") 
    st.session_state.company_id = params.get("company_id")

# -----------------------------
# LOGIN
# -----------------------------
logged = login()

if not logged:
    st.title(APP_NAME)
    st.caption("Inicia sesión para continuar")
    st.stop()

# -----------------------------
# VALIDACIÓN DE SESIÓN (ANTES DE TODO)
# -----------------------------
if "user" not in st.session_state:
    st.error("Sesión inválida. Vuelve a iniciar sesión.")
    st.stop()

# -----------------------------
# CONTEXTO (COMPANY → SITE)
# -----------------------------
from modules.sites.service import list_sites, add_site

company_id = st.session_state.get("company_id")
sites = list_sites(company_id)

st.sidebar.markdown("### 🏭 Sitios")

# -----------------------------
# CREAR SITE (SIDEBAR)
# -----------------------------
new_site = st.sidebar.text_input("Nuevo sitio", key="new_site")

if st.sidebar.button("➕ Crear sitio"):
    if new_site:
        add_site(new_site, company_id)
        st.sidebar.success("Site creado")
        st.rerun()
    else:
        st.sidebar.warning("Ingresa un nombre")

# -----------------------------
# LISTA DE SITES
# -----------------------------
if not sites:
    st.title("Dashboard")
    st.info("Crea tu primer sitio para comenzar")
    st.stop()

# 🔥 usar IDs (correcto)
site_options = {s["name"]: s["id"] for s in sites}

selected_site_name = st.sidebar.selectbox(
    "Selecciona sitio",
    list(site_options.keys()),
    key="site_selector"
)

site_id = site_options[selected_site_name]
st.session_state.site_id = site_id

# -----------------------------
# ASSETS
# -----------------------------
from modules.assets.service import list_assets, add_asset

st.subheader("Assets")

new_asset = st.text_input("Nombre del asset")
asset_type = st.text_input("Tipo")

if st.button("Crear asset", key="btn_create_asset"):
    if new_asset:
        add_asset(new_asset, asset_type, site_id)
        st.success("Asset creado")
        st.rerun()
    else:
        st.warning("Ingresa un nombre de asset")

assets = list_assets(site_id)

if not assets:
    st.info("No hay assets en este sitio")
    st.stop()

st.divider()

# -----------------------------
# SELECTOR DE ASSET
# -----------------------------
asset_options = {a["name"]: a["id"] for a in assets}

selected_asset_name = st.selectbox(
    "Selecciona asset",
    list(asset_options.keys()),
    key="asset_selector"
)
st.markdown(f"### 📍 Asset: {selected_asset_name}")
asset_id = asset_options[selected_asset_name]

# -----------------------------
# READINGS
# -----------------------------
from modules.readings.service import add_reading, list_readings

st.subheader("Nueva medición")

# -----------------------------
# CARGA DESDE EXCEL
# -----------------------------
from modules.readings.service import load_readings_from_excel

st.subheader("Cargar lecturas desde Excel")

archivo = st.file_uploader("Subir archivo Excel", type=["xlsx"])

if archivo:
    if st.button("📥 Cargar Excel"):
        ok, msg = load_readings_from_excel(asset_id, archivo)

        if ok:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

col1, col2, col3 = st.columns(3)

date = col1.date_input("Fecha")
ph = col1.number_input("pH", min_value=0.0, max_value=14.0, value=7.0)

temperature_c = col2.number_input("Temperatura", min_value=0.0, value=25.0)
tds_ppm = col2.number_input("TDS", min_value=1.0)

calcium_hardness = col3.number_input("Calcio", min_value=1.0)
alkalinity = col3.number_input("Alcalinidad", min_value=1.0)

if st.button("Guardar lectura", key="btn_save_reading"):
    add_reading(asset_id, {
        "date": date.isoformat(),
        "ph": ph,
        "temperature": temperature_c,
        "tds": tds_ppm,
        "calcium": calcium_hardness,
        "alkalinity": alkalinity
    })
    st.success("Lectura guardada")
    st.rerun()

# -----------------------------
# BORRAR HISTORIAL
# -----------------------------
from modules.readings.service import clear_readings

if st.button("🗑️ Borrar historial", key="btn_delete_readings"):
    if ENV == "prod":
        st.error("No puedes borrar datos en producción")
    else:
        clear_readings(asset_id)
        st.success("Historial eliminado")
        st.rerun()



# -----------------------------
# HISTORIAL + LSI
# -----------------------------
from modules.analytics.service import calcular_lsi, clasificar_lsi
import pandas as pd

readings = list_readings(asset_id)

st.subheader("Historial")

if readings:
    #para ordenar historial
    df = pd.DataFrame(readings).sort_values("date")
    df = df.dropna()

    if not df.empty:
        df["LSI"] = df.apply(
            lambda row: calcular_lsi(
                row["ph"],
                row["temperature"],
                row["tds"],
                row["calcium"],
                row["alkalinity"]
            ),
            axis=1
        )

        df["Estado"] = df["LSI"].apply(clasificar_lsi)
        from modules.analytics.service import recomendaciones_lsi

        df["Recomendación"] = df.apply(recomendaciones_lsi, axis=1)
        from modules.analytics.service import tendencia_lsi, proyectar_lsi

        estado_tendencia, slope = tendencia_lsi(df)
        proyeccion = proyectar_lsi(df)
        # -----------------------------
        # DASHBOARD PRO
        # -----------------------------
        import plotly.express as px

        st.divider()

        # 🔥 ÚLTIMO REGISTRO
        ultimo = df.iloc[-1]

        col1, col2, col3 = st.columns(3)

        # KPI
        col1.metric("LSI actual", round(ultimo["LSI"], 2))
        
        # ESTADO TEXTO
        col2.metric("Estado", ultimo["Estado"])

        # SEMÁFORO
        estado = ultimo["Estado"]

        if estado == "Estable":
            col3.success("🟢 Sistema estable")
        elif estado == "Incrustante":
            col3.error("🔴 Riesgo de incrustación")
        else:
            col3.warning("🔵 Riesgo de corrosión")

        # -----------------------------
        # ALERTA AUTOMÁTICA
        # -----------------------------
        if ultimo["LSI"] > 0.5:
            st.error("⚠️ Agua incrustante — riesgo de depósitos")
        elif ultimo["LSI"] < -0.5:
            st.warning("⚠️ Agua corrosiva — riesgo de daño")
        else:
            st.success("Sistema en equilibrio")
        
        st.subheader("🧠 Recomendación")
        st.info(ultimo["Recomendación"])

        st.subheader("📊 Tendencia")
        st.info(f"{estado_tendencia}")

        st.dataframe(df)

        from modules.analytics.service import calcular_componentes

        df[["A", "B", "C", "D"]] = df.apply(
            lambda row: pd.Series(calcular_componentes(row)),
            axis=1
        )

        df = df[
            ["date", "ph", "temperature", "tds", "calcium", "alkalinity",
            "A", "B", "C", "D", "LSI", "Estado", "Recomendación"]
        ]
        # -----------------------------
        # EXPORTAR A EXCEL
        # -----------------------------
        import io

        st.subheader("📥 Exportar historial")

        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Historial")

        excel_data = output.getvalue()

        st.download_button(
            label="⬇️ Descargar Excel",
            data=excel_data,
            file_name="historial_water_analytics.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        # -----------------------------
        # GRÁFICA LSI (MEJORADA)
        # -----------------------------
        import plotly.express as px

        st.subheader("📈 LSI vs Tiempo")

        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        

        # gráfico
        fig = px.scatter(
            df,
            x="date",
            y="LSI",
            color="Estado",  # 🔥 magia aquí
            title="LSI vs Tiempo",
        )

        # -----------------------------
        # 🔮 PROYECCIÓN FUTURA
        # -----------------------------
        if proyeccion:
            last_date = df["date"].max()

            future_dates = pd.date_range(
                start=last_date,
                periods=len(proyeccion) + 1,
                freq="D"
            )[1:]

            fig.add_scatter(
                x=future_dates,
                y=proyeccion,
                mode="lines+markers",
                name="Proyección",
                line=dict(dash="dot")
            )

        # zona ideal
        fig.add_hrect(
            y0=-0.5,
            y1=0.5,
            fillcolor="green",
            opacity=0.15,
            line_width=0,
        )

        # línea equilibrio
        fig.add_hline(
            y=0,
            line_dash="dash"
        )

        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No hay lecturas registradas")

st.subheader("📊 Ventana Operativa (Estado Estable)")

df_estable = df[df["Estado"] == "ideal"]

if not df_estable.empty:

    resumen = {
        "pH": (df_estable["ph"].min(), df_estable["ph"].max()),
        "Temperatura": (df_estable["temperature"].min(), df_estable["temperature"].max()),
        "TDS": (df_estable["tds"].min(), df_estable["tds"].max()),
        "Calcio": (df_estable["calcium"].min(), df_estable["calcium"].max()),
        "Alcalinidad": (df_estable["alkalinity"].min(), df_estable["alkalinity"].max()),
        "LSI": (df_estable["LSI"].min(), df_estable["LSI"].max())
    }

    for k, v in resumen.items():
        st.write(f"{k}: {round(v[0],2)} – {round(v[1],2)}")

else:
    st.info("No hay suficientes datos en estado estable")    

#if len(df_estable) < 20:
    #st.warning("⚠️ Se requieren al menos 20 datos en estado estable para definir la ventana operativa")

