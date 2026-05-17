import streamlit as st
import pandas as pd

from modules.operator.repository import (
    get_company_dashboard_data
)


def operator_dashboard():

    user = st.session_state.get(
        "user"
    )

    # ======================================
    # VALIDAR SESIÓN
    # ======================================
    if not isinstance(user, dict):

        st.error(
            "Sesión inválida. "
            "Vuelve a iniciar sesión."
        )

        return

    company_id = user.get(
        "company_id"
    )

    # ======================================
    # DATA
    # ======================================
    data = get_company_dashboard_data(
        company_id
    )

    st.title(
        "📊 Dashboard Operativo"
    )

    if not data:

        st.warning(
            "No hay información"
        )

        return

    # ======================================
    # EMPRESA
    # ======================================
    company_name = data[0][
        "company_name"
    ]
    # ======================================
    # SIDEBAR EMPRESA
    # ======================================  
    st.sidebar.subheader(
        "🏭 Empresa"
    )

    st.sidebar.success(
        company_name
    )

    # ======================================
    # SISTEMAS
    # ======================================
    system_options = {

        row["system_name"]: row

        for row in data
    }

    st.divider()
    
    selected_system = st.sidebar.selectbox(
        "--Selecciona un sistema para continuar--",
        list(system_options.keys())
    )

    # ======================================
    # SISTEMA SELECCIONADO
    # ======================================
    system = system_options[
        selected_system
    ]

    # ======================================
    # INFO SISTEMA SIDEBAR
    # ======================================
    st.sidebar.markdown(
        f"""
        ### 
        ⚙️ **Tipo:**  
        {system['asset_type']}

        🧪 **Método químico:**  
        {system['chemistry_model']}
        """
    )
    st.subheader(
        f"📍 {system['system_name']}"
    )
    # ======================================
    # DASHBOARD PRINCIPAL
    # ======================================
    col_left, col_right = st.columns(
        [1, 3]
    )

    # ======================================
    # LEFT
    # ======================================
    with col_left:



        # ==================================
        # MÉTODO QUÍMICO
        # ==================================
        chemistry_model = system[
            "chemistry_model"
        ]

        # ==================================
        # LSI
        # ==================================
        if "LSI" in chemistry_model:

            lsi_method = st.selectbox(
                "Selecciona método cálculo LSI",
                [
                    "LSI Logarítmico",
                    "LSI Tablas",
                    "Comparación LSI"
                ]
            )

            # ------------------------------
            # LOG
            # ------------------------------
            if lsi_method == (
                "LSI Logarítmico"
            ):

                st.info(
                    """
                    Sistema usando:

                    LSI Logarítmico
                    """
                )

            # ------------------------------
            # TABLAS
            # ------------------------------
            elif lsi_method == (
                "LSI Tablas"
            ):

                st.info(
                    """
                    Sistema usando:

                    LSI Tablas
                    """
                )

            # ------------------------------
            # COMPARACIÓN
            # ------------------------------
            elif lsi_method == (
                "Comparación LSI"
            ):

                st.info(
                    """
                    Comparación entre:

                    • LSI Logarítmico
                    • LSI Tablas
                    """
                )

        # ==================================
        # RSI
        # ==================================
        elif "RSI" in chemistry_model:

            st.info(
                """
                Sistema configurado
                para índice Ryznar
                """
            )

    # ======================================
    # RIGHT
    # ======================================
    with col_right:

        st.subheader(
            "📘 Información"
        )

        st.text_area(
            "Información técnica",
            value="""
    Aquí puedes agregar:

    • teoría química
    • interpretación
    • recomendaciones
    • límites operativos
    • criterios de corrosión
    • criterios de incrustación
            """,
            height=250
        )

        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/3/3d/Cooling_tower.jpg",
            caption="Sistema de enfriamiento"
        )

    st.divider()

   