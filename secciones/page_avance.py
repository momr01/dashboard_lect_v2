import streamlit as st
import plotly.express as px
from graficos import graf_ev_lect

def page_avance(df_filtrado):
    st.title("Avance de Descarga")

    graf_ev_lect(
        df_filtrado,
        col_leidos="total_leidos_actual",
        titulo="Evolución diaria de lecturas s/fecha actual",
        key="ev_filtrado_actual_val_10",
        titulo_col_leidos="Lecturas realizadas",
        mostrar_val=True
    )

   