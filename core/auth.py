import streamlit as st

def is_admin():
    return st.session_state.get("role") == "admin"