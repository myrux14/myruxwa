import streamlit as st
from core.auth import is_admin
from core.database import get_connection
from modules.auth.repository import create_user
from modules.auth.repository import reset_password
from modules.auth.repository import (
    get_all_users,
    create_user,
    update_user,
    toggle_user,
    delete_user
)

def admin_panel():
    if not is_admin():
        st.error("Acceso restringido")
        st.stop()

    st.title("⚙️ Panel de Administración")

    tab1, tab2 = st.tabs(["Usuarios", "Base de datos"])

    # -----------------------------
    # TAB USUARIOS
    # -----------------------------
    with tab1:

        # 🔹 COMPANIES
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM companies")
        companies = cursor.fetchall()
        cursor.close()
        conn.close()

        company_map = {c[1]: c[0] for c in companies}

        # -----------------------------
        # CREAR USUARIO
        # -----------------------------
        st.subheader("➕ Crear usuario")

        with st.form("create_user"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            role = st.selectbox("Rol", ["admin", "operator"])
            company_name = st.selectbox("Empresa", list(company_map.keys()))

            if st.form_submit_button("Crear"):
                ok, msg = create_user(
                    username,
                    password,
                    role,
                    company_map[company_name]
                )
                st.success(msg) if ok else st.error(msg)
                st.rerun()

        st.divider()

        # -----------------------------
        # LISTADO + CRUD
        # -----------------------------
        st.subheader("👥 Usuarios")

        users = get_all_users()

        for u in users:
            with st.expander(f"{u['username']} (ID {u['id']})"):

                col1, col2 = st.columns(2)

                # -----------------------------
                # EDITAR
                # -----------------------------
                with col1:
                    new_role = st.selectbox(
                        "Rol",
                        ["admin", "operator"],
                        index=0 if u["role"] == "admin" else 1,
                        key=f"role_{u['id']}"
                    )

                    new_company = st.number_input(
                        "Company ID",
                        value=u["company_id"],
                        key=f"comp_{u['id']}"
                    )

                    if st.button("Actualizar", key=f"upd_{u['id']}"):
                        ok, msg = update_user(u["id"], new_role, new_company)
                        st.success(msg) if ok else st.error(msg)
                        st.rerun()

                # -----------------------------
                # ACCIONES
                # -----------------------------
                with col2:
                    if st.button(
                        "Desactivar" if u["active"] else "Activar",
                        key=f"toggle_{u['id']}"
                    ):
                        ok, msg = toggle_user(u["id"], 0 if u["active"] else 1)
                        st.success(msg) if ok else st.error(msg)
                        st.rerun()

                    if st.button("Eliminar", key=f"del_{u['id']}"):
                        ok, msg = delete_user(u["id"])
                        st.warning(msg) if ok else st.error(msg)
                        st.rerun()

                # -----------------------------
                # RESET PASSWORD 🔐
                # -----------------------------
                st.markdown("### 🔐 Reset contraseña")

                col3, col4 = st.columns(2)

                with col3:
                    new_pass = st.text_input(
                        "Nueva contraseña",
                        type="password",
                        key=f"pass_{u['id']}"
                    )

                with col4:
                    confirm_pass = st.text_input(
                        "Confirmar contraseña",
                        type="password",
                        key=f"pass2_{u['id']}"
                    )

                if st.button("Actualizar contraseña", key=f"reset_{u['id']}"):

                    if not new_pass:
                        st.warning("Ingresa una contraseña")
                    elif new_pass != confirm_pass:
                        st.error("Las contraseñas no coinciden")
                    else:
                        ok, msg = reset_password(u["id"], new_pass)

                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    
                    
    # -----------------------------
    # TAB DB
    # -----------------------------
    with tab2:
        st.subheader("Migraciones")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM migrations")
        data = cursor.fetchall()

        st.dataframe(data)

        cursor.close()
        conn.close()