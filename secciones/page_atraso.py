import streamlit as st
import plotly.express as px
from helpers.btn_excel_csv import btn_excel_csv

def page_atraso(color, emoji, estado, kpi_atraso, df_base, realvsprog):
    st.title("Atraso")

    
    #st.space("large") # Añade un espacio grande
    st.subheader("Estado operativo")

    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:25px;
            border-radius:12px;
            text-align:center;
            color:white;
            font-size:28px;
            font-weight:bold;
        ">
            {emoji} {estado} <br>
            Atraso: {kpi_atraso:.2f} días
        </div>
        """,
        unsafe_allow_html=True
    )

    st.space("large") # Añade un espacio grande

    st.subheader("Proyección de cumplimiento del período")

            # df_proy = df_filtrado.groupby(df_filtrado["f_lteor"].dt.date).agg({
            #     "total_programados": "sum",
            #     "total_leidos_ftl": "sum"
            # }).reset_index()
    df_proy = df_base.groupby(df_base["f_lteor"].dt.date).agg({
                "total_programados": "sum",
                "total_leidos_ftl": "sum"
            }).reset_index()

    df_proy = df_proy.rename(columns={"f_lteor":"fecha",  "leidos_acum":"Lecturas acumuladas",
                "ritmo_ideal":"Ritmo ideal"})

            # acumulados
    df_proy["prog_acum"] = df_proy["total_programados"].cumsum()
    df_proy["leidos_acum"] = df_proy["total_leidos_ftl"].cumsum()



    total_prog_periodo = df_proy["total_programados"].sum()

    df_proy["ritmo_ideal"] = (
                total_prog_periodo / len(df_proy)
            ) * (df_proy.index + 1)





    st.line_chart(
                df_proy.set_index("fecha")[[
                    "leidos_acum",
                    "ritmo_ideal"
                ]]
            )

            # df_proy = df_proy.rename(columns={
            #     "leidos_acum":"Lecturas acumuladas",
            #     "ritmo_ideal":"Ritmo ideal"
            # })



    st.space("large") # Añade un espacio grande

    st.subheader("Real vs Programado")
    st.dataframe(realvsprog, use_container_width=True, hide_index=True)

    btn_excel_csv(realvsprog, "real_vs_prog")