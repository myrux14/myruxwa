import pandas as pd
import streamlit as st
from modules.analytics.service import calcular_lsi, clasificar_lsi
from modules.analytics.service import calcular_lsi_dual
from modules.analytics.ui import render_lsi_charts
from core.optimizer import ajustar_parametros

# 🔥 SIEMPRE PRIMERO
st.set_page_config(page_title="Water Analytics", layout="wide")
from core.migrations import run_migrations
run_migrations()

# ahora sí imports
from core.config import APP_NAME, ENV
from core.database import init_db
from modules.auth.ui import login

# UI ENV
st.sidebar.info(f"Entorno: {ENV}")

# init solo en local
if ENV == "local" and "db_initialized" not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

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
from core.env_check import check_environment

db_info = check_environment()

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

# =========================================
# ROUTER PRINCIPAL POR ROL
# =========================================
role = st.session_state.get("role")

# -----------------------------
# ADMIN
# -----------------------------
if role == "admin":

    from modules.admin.ui import admin_panel

    admin_panel()

    st.stop()

# -----------------------------
# OPERATOR
# -----------------------------
elif role == "operator":

    from modules.operations.ui import (
        operator_dashboard
    )

    operator_dashboard()

    st.stop()

# -----------------------------
# VIEWER
# -----------------------------
elif role == "viewer":

    st.warning(
        "Dashboard viewer pendiente"
    )

    st.stop()

# -----------------------------
# ROL INVÁLIDO
# -----------------------------
else:

    st.error("Rol inválido")
    st.stop()



