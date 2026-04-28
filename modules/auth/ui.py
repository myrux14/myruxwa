# modules/auth/ui.py

import streamlit as st
from modules.auth.service import login_user
import uuid


def logout():
    st.query_params.clear()
    st.session_state.clear()
    st.session_state.logged_in = False


def login():

    st.sidebar.markdown("### 🔐 Cuenta")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # -----------------------------
    # SESIÓN ACTIVA
    # -----------------------------
    if st.session_state.get("logged_in", False):

        st.sidebar.success(f"👤 {st.session_state.get('user')}")

        if st.sidebar.button("Cerrar sesión"):
            logout()
            st.rerun()

        return True

    # -----------------------------
    # LOGIN
    # -----------------------------
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")

    if st.sidebar.button("Entrar"):

        user = login_user(username, password)

        if user == "inactive":
            st.sidebar.error("Usuario desactivado")

        elif user:
            token = str(uuid.uuid4())

            st.session_state.logged_in = True
            st.session_state.user = user["username"]
            st.session_state.role = user["role"]
            st.session_state.company_id = user["company_id"]
            st.session_state.token = token

            st.query_params.update({
                "token": token,
                "user": user["username"],
                "role": user["role"],
                "company_id": str(user["company_id"])
            })

            st.rerun()

        else:
            st.sidebar.error("Credenciales incorrectas")

    return st.session_state.logged_in