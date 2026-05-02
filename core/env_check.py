import streamlit as st
from core.config import ENV, get_db_info


def check_environment():
    info = get_db_info()

    st.sidebar.markdown("### 🌍 Entorno")

    st.sidebar.info(f"""
ENV: {ENV}
DB: {info['db']}
HOST: {info['host']}
USER: {info['user']}
""")

    # 🔴 ALERTA SI ESTÁS EN PRODUCCIÓN CON DB LOCAL
    if ENV == "production" and "localhost" in info["host"]:
        st.sidebar.error("⚠️ Producción usando DB local")

    # 🔴 ALERTA SI ESTÁS EN LOCAL CON DB DE PRODUCCIÓN
    if ENV == "local" and "render" in info["host"]:
        st.sidebar.warning("⚠️ Estás usando DB de producción en local")

    return info