import streamlit as st
import pandas as pd
import plotly.express as px

def page_pend(tpl):
    st.title("% Pendientes")

    
    # st.space("large") # Añade un espacio grande
    # st.subheader("Datos filtrados s/ mes y tarifa")
    # st.dataframe(tpl, use_container_width=True)
    # st.dataframe(tpl, hide_index=True)















    # st.space("large")
    # # st.subheader("Datos filtrados s/ mes y tarifa")

    # # selector
    # filtro = st.selectbox(
    #     "Filtrar demora hábil sin feriados",
    #     ["Todos", ">= 0", "= 0"]
    # )

    # tpl["demora_hab_sin_feriados"] = pd.to_numeric(
    #     tpl["demora_hab_sin_feriados"],
    #     errors="coerce"
    # )



    # # aplicar filtro
    # if filtro == ">= 0":
    #     tpl_filtrado = tpl[tpl["demora_hab_sin_feriados"] >= 0]
    # elif filtro == "= 0":
    #     tpl_filtrado = tpl[tpl["demora_hab_sin_feriados"] == 0]
    # else:
    #     tpl_filtrado = tpl

    # mostrar
    # st.dataframe(tpl_filtrado, use_container_width=True, hide_index=True)

















    # st.space("large")
    st.subheader("Estado de Lecturas")

    # -------------------------
    # LIMPIEZA CLAVE
    # -------------------------
    tpl["demora_hab_sin_feriados"] = pd.to_numeric(
        tpl["demora_hab_sin_feriados"],
        errors="coerce"
    )

    tpl["contratista"] = (
        tpl["contratista"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    tpl["tarifa"] = (
        tpl["tarifa"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # tpl["desc_est"] = (
    #     tpl["desc_est"]
    #     .astype(str)
    #     .str.strip()
    #     .str.upper()
    # )

    # -------------------------
    # FILTROS
    # -------------------------

    # filtro demora
    filtro_demora = st.selectbox(
        "Filtrar demora hábil",
        ["Todos", ">= 1", ">= 0", "= 0"]
    )

    # filtro contratista (multiselección)
    contratistas = st.multiselect(
        "Seleccionar contratista",
        ["SYMESA", "ERLYFSA", "PAMAR"],
        default=["SYMESA", "ERLYFSA", "PAMAR"]
    )

    tarifas = st.multiselect(
        "Seleccionar tarifa",
        ["T1", "T2", "T3"],
        default=["T1", "T2"]
    )

    estados_tpl = st.multiselect(
        "Seleccionar estado de TPL",
        ["Enviado al TPL", "Recibido del TPL", "Cargado TPL"],
        default=["Enviado al TPL", "Cargado TPL"]
    )


    # columnas a ocultar
    columnas_ocultas = [
        "anio_ciclo",
        "nl_gen",
        "est_itin",
        "anomalias",
        "prop_anomalias",
        "demora_dias_corridos",
        "cod_contratista"
    ]

    # columnas permitidas
    columnas_disponibles = [
        col for col in tpl.columns
        if col not in columnas_ocultas
    ]

    # selector columnas visibles
    columnas_visibles = st.multiselect(
        "Columnas visibles",
        options=columnas_disponibles,
        default=columnas_disponibles
    )

    # -------------------------
    # APLICAR FILTROS
    # -------------------------

    tpl_filtrado = tpl.copy()

    # filtro demora
    if filtro_demora == ">= 0":
        tpl_filtrado = tpl_filtrado[
            tpl_filtrado["demora_hab_sin_feriados"] >= 0
        ]
    elif filtro_demora == "= 0":
        tpl_filtrado = tpl_filtrado[
            tpl_filtrado["demora_hab_sin_feriados"] == 0
        ]
    elif filtro_demora == ">= 1":
        tpl_filtrado = tpl_filtrado[
            tpl_filtrado["demora_hab_sin_feriados"] >= 1
        ]

    # filtro contratista
    tpl_filtrado = tpl_filtrado[
        tpl_filtrado["contratista"].isin(contratistas)
    ]


    tpl_filtrado = tpl_filtrado[
        tpl_filtrado["tarifa"].isin(tarifas)
    ]

    tpl_filtrado = tpl_filtrado[
        tpl_filtrado["desc_est"].isin(estados_tpl)
    ]

    tpl_filtrado = tpl_filtrado[
        columnas_visibles
    ]

    tpl_filtrado = tpl_filtrado.rename(columns={
        "demora_hab_sin_feriados": "demora"
    })

    # -------------------------
    # RESULTADO
    # -------------------------
    st.dataframe(tpl_filtrado, use_container_width=True, hide_index=True)


    from io import BytesIO

    # convertir a excel en memoria
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        tpl_filtrado.to_excel(writer, index=False, sheet_name="Datos")

    excel_data = output.getvalue()

    # botón descarga
    # st.download_button(
    #     label="📥 Descargar Excel",
    #     data=excel_data,
    #     file_name="datos_filtrados.xlsx",
    #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # )



    #######################

    csv = tpl_filtrado.to_csv(index=False).encode("utf-8")

    # st.download_button(
    #     label="📥 Descargar CSV",
    #     data=csv,
    #     file_name="datos_filtrados.csv",
    #     mime="text/csv"
    # )


    col1, col2 = st.columns(2)

    with col1:
        # botón 
        # botón descarga
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_data,
            file_name="datos_filtrados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="btn-excel"
        )

    with col2:
        # botón csv
            st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name="datos_filtrados.csv",
            mime="text/csv",
            key="btn-csv"
        )

    

   
   