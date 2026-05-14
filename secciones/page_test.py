import streamlit as st
import plotly.express as px
from datetime import timedelta
from graficos import graf_proyeccion_atraso, graf_ev_lect_atraso_ritmo, graf_ev_lect

def page_test(df_filtrado, dias_transcurridos, total_programados, hoy,
              df_base, dias_restantes, lecturas_pendientes_total, df):
    st.title("TESTING")



    st.space("large") # Añade un espacio grande
    # lecturas realizadas hasta hoy
    lecturas_realizadas = df_filtrado["total_leidos_ftl"].sum()

    # ritmo actual (lecturas por día)
    ritmo_actual = (
        lecturas_realizadas / dias_transcurridos
        if dias_transcurridos > 0 else 0
    )

    # lecturas pendientes
    lecturas_pendientes = total_programados - lecturas_realizadas

    # días necesarios al ritmo actual
    dias_necesarios = (
        lecturas_pendientes / ritmo_actual
        if ritmo_actual > 0 else 0
    )

    fecha_estimada_fin = hoy + timedelta(days=dias_necesarios)

    st.subheader("Proyección de finalización")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Ritmo actual",
            f"{ritmo_actual:.0f} lecturas/día"
        )

    with col2:
        st.metric(
            "Días necesarios",
            f"{dias_necesarios:.1f}"
        )

    with col3:
        st.metric(
            "Fecha estimada de finalización",
            fecha_estimada_fin.strftime("%d-%m-%Y")
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
    st.subheader("Evolución del backlog")

    # df_backlog = df_filtrado.groupby(df_filtrado["f_lteor"].dt.date).agg({
    #     "total_programados": "sum",
    #     "total_leidos_ftl": "sum"
    # }).reset_index()
    df_backlog = df_base.groupby(df_base["f_lteor"].dt.date).agg({
        "total_programados": "sum",
        "total_leidos_ftl": "sum"
    }).reset_index()

    df_backlog = df_backlog.rename(columns={"f_lteor": "fecha"})

    df_backlog["prog_acum"] = df_backlog["total_programados"].cumsum()
    df_backlog["leidos_acum"] = df_backlog["total_leidos_ftl"].cumsum()

    df_backlog["backlog"] = df_backlog["prog_acum"] - df_backlog["leidos_acum"]


    st.line_chart(
        df_backlog.set_index("fecha")[["backlog"]]
    )
















    graf_proyeccion_atraso(
        df_base,
        col_leidos="total_leidos_ftl",
        titulo="Proyección de atraso lecturas FTL",
        key="graf_atraso_ftl"
    )


    graf_proyeccion_atraso(
        df_filtrado,
        col_leidos="total_leidos_ftl",
        titulo="Proyección de atraso lecturas FTL",
        key="graf_atraso_ftl2"
    )




    


    st.space("large") # Añade un espacio grande
    st.subheader("Top 10 días con mayor atraso")

    # df_dias = df_filtrado.groupby(df_filtrado["f_lteor"].dt.date).agg({
    #     "total_programados":"sum",
    #     "total_leidos_ftl":"sum"
    # }).reset_index()

    df_dias = df_base.groupby(df_base["f_lteor"].dt.date).agg({
        "total_programados":"sum",
        "total_leidos_ftl":"sum"
    }).reset_index()

    df_dias["atraso"] = (
        df_dias["total_programados"] -
        df_dias["total_leidos_ftl"]
    )


    top_atrasos = df_dias.sort_values(
        "atraso",
        ascending=False
    ).head(10)

    st.dataframe(
        top_atrasos,
        use_container_width=True
    )


























    # lecturas_realizadas = df_filtrado["total_leidos_ftl"].sum()
    lecturas_realizadas = df_base["total_leidos_ftl"].sum()

    ritmo_actual = (
        lecturas_realizadas / dias_transcurridos
        if dias_transcurridos > 0 else 0
    )


    lecturas_pendientes = total_programados - lecturas_realizadas


    capacidad_restante = ritmo_actual * dias_restantes

    atraso_final = lecturas_pendientes - capacidad_restante

    st.space("large") # Añade un espacio grande
    st.subheader("Predicción de atraso al cierre")

    if atraso_final <= 0:
        st.success(
            f"🟢 El período terminaría al día o adelantado"
        )
    else:
        st.error(
            f"🔴 Atraso proyectado: {int(atraso_final)} lecturas"
        )

















    st.space("large") # Añade un espacio grande
    st.subheader("Evolución diaria de lecturas")

    df_evol = df_base.groupby(df_base["f_lteor"].dt.date).agg({
        "total_programados":"sum",
        "total_leidos_ftl":"sum"
    }).reset_index()

    df_evol = df_evol.rename(columns={"f_lteor":"fecha"})

    df_graf = df_evol.rename(columns={
        "total_programados": "Lecturas programadas",
        "total_leidos_ftl": "Lecturas realizadas s/FTL"
    })

    # import plotly.express as px

    df_graf["Atraso diario"] = (
        df_graf["Lecturas programadas"] -
        df_graf["Lecturas realizadas s/FTL"]
    )

    total_programado_periodo = df_graf["Lecturas programadas"].sum()
    total_dias = len(df_graf)

    df_graf["dia_n"] = range(1, total_dias + 1)

    df_graf["Ritmo ideal"] = (
        total_programado_periodo / total_dias
    ) * df_graf["dia_n"]





#############################################################################



    graf_ev_lect_atraso_ritmo(
        df_base,
        col_leidos="total_leidos_ftl",
        titulo="Evolución diaria de lecturas s/FTL",
        titulo_col_leidos="Lecturas realizadas s/FTL",
        key="grafico_ftl"
    )

    graf_ev_lect_atraso_ritmo(
        df_base,
        col_leidos="total_leidos_actual",
        titulo="Evolución diaria de lecturas s/fecha actual",
        titulo_col_leidos="Lecturas realizadas s/fecha actual",
        key="grafico_ftl2"
    )

    graf_ev_lect_atraso_ritmo(
        df_filtrado,
        col_leidos="total_leidos_ftl",
        titulo="Evolución diaria de lecturas s/FTL",
        titulo_col_leidos="Lecturas realizadas s/FTL",
        key="grafico_ftl3"
    )

    graf_ev_lect_atraso_ritmo(
        df_filtrado,
        col_leidos="total_leidos_actual",
        titulo="Evolución diaria de lecturas s/fecha actual",
        titulo_col_leidos="Lecturas realizadas s/fecha actual",
        key="grafico_ftl4"
    )
















    lecturas_realizadas = df_graf["Lecturas realizadas s/FTL"].sum()

    dias_transcurridos = len(df_graf)

    ritmo_actual = (
        lecturas_realizadas / dias_transcurridos
        if dias_transcurridos > 0 else 0
    )


    total_programado = df_graf["Lecturas programadas"].sum()

    dias_estimados = (
        total_programado / ritmo_actual
        if ritmo_actual > 0 else 0
    )

    #from datetime import timedelta

    fecha_inicio = df_graf["fecha"].min()

    fecha_fin_estimada = fecha_inicio + timedelta(days=int(dias_estimados))

    st.metric(
        "📅 Fecha estimada de finalización",
        fecha_fin_estimada.strftime("%d-%m-%Y")
    )










    fecha_fin_programada = df_graf["fecha"].max()

    desvio = (fecha_fin_estimada - fecha_fin_programada).days


    st.metric(
        "⏱ Desvío estimado",
        f"{desvio} días",
        delta=desvio
    )












    ritmo_necesario = (
        lecturas_pendientes_total / dias_restantes
        if dias_restantes > 0 else 0
    )

    ratio_ritmo = (
        ritmo_actual / ritmo_necesario
        if ritmo_necesario > 0 else 1
    )


    # ratio >= 1     → ritmo suficiente
    # ratio 0.8-1    → riesgo medio
    # ratio < 0.8    → riesgo alto

    if ratio_ritmo >= 1:
        estado = "🟢 Bajo riesgo"
        color = "green"
    elif ratio_ritmo >= 0.8:
        estado = "🟡 Riesgo medio"
        color = "orange"
    else:
        estado = "🔴 Alto riesgo"
        color = "red"


    st.subheader("Indicador de riesgo operativo")

    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:20px;
            border-radius:10px;
            text-align:center;
            font-size:22px;
            color:white;
            font-weight:bold;
        ">
            {estado}
        </div>
        """,
        unsafe_allow_html=True
    )


































    st.space("large") # Añade un espacio grande
    st.subheader("Evolución diaria de lecturas")

    # df_evol = df_base.groupby(df_base["f_lteor"].dt.date).agg({
    #     "total_programados":"sum",
    #     "total_leidos_ftl":"sum"
    # }).reset_index()

    # df_evol = df_evol.rename(columns={"f_lteor":"fecha"})

    # df_graf = df_evol.rename(columns={
    #     "total_programados": "Lecturas programadas",
    #     "total_leidos_ftl": "Lecturas realizadas s/FTL"
    # })

    # # import plotly.express as px

    # fig = px.line(
    #     df_graf,
    #     x="fecha",
    #     y=["Lecturas programadas", "Lecturas realizadas s/FTL"],
    #     labels={
    #         "fecha": "Día de lectura",
    #         "value": "Cantidad de lecturas",
    #         "variable": "Tipo"
    #     },
    #      markers=True,
    #        title="Evolución diaria de lecturas s/FTL"
    # )

    # fig.update_layout(
    #     yaxis=dict(
    #         tickformat=","
    #     )
    # )

    # st.plotly_chart(fig, use_container_width=True, key="todo_ftl")





    graf_ev_lect(
            df_base,
            col_leidos="total_leidos_ftl",
            titulo="Evolución diaria de lecturas s/FTL",
            key="ev_todo_ftl",
            titulo_col_leidos="Lecturas realizadas s/FTL"
        )


    graf_ev_lect(
            df_base,
            col_leidos="total_leidos_actual",
            titulo="Evolución diaria de lecturas s/fecha actual",
            key="ev_todo_actual",
            titulo_col_leidos="Lecturas realizadas"
        )

    graf_ev_lect(
            df_filtrado,
            col_leidos="total_leidos_ftl",
            titulo="Evolución diaria de lecturas s/FTL",
            key="ev_filtrado_ftl",
            titulo_col_leidos="Lecturas realizadas s/FTL"
        )


    graf_ev_lect(
            df_filtrado,
            col_leidos="total_leidos_actual",
            titulo="Evolución diaria de lecturas s/fecha actual",
            key="ev_filtrado_actual",
            titulo_col_leidos="Lecturas realizadas"
        )





    graf_ev_lect(
            df_base,
            col_leidos="total_leidos_ftl",
            titulo="Evolución diaria de lecturas s/FTL",
            key="ev_todo_ftl_val",
            titulo_col_leidos="Lecturas realizadas s/FTL",
            mostrar_val=True
        )


    graf_ev_lect(
            df_base,
            col_leidos="total_leidos_actual",
            titulo="Evolución diaria de lecturas s/fecha actual",
            key="ev_todo_actual_val",
            titulo_col_leidos="Lecturas realizadas",
            mostrar_val=True
        )

    graf_ev_lect(
            df_filtrado,
            col_leidos="total_leidos_ftl",
            titulo="Evolución diaria de lecturas s/FTL",
            key="ev_filtrado_ftl_val",
            titulo_col_leidos="Lecturas realizadas s/FTL",
            mostrar_val=True
        )


    graf_ev_lect(
            df_filtrado,
            col_leidos="total_leidos_actual",
            titulo="Evolución diaria de lecturas s/fecha actual",
            key="ev_filtrado_actual_val",
            titulo_col_leidos="Lecturas realizadas",
            mostrar_val=True
        )































    # st.space("large") # Añade un espacio grande
    # st.subheader("Evolución diaria de lecturas")

    # df_evol = df_base.groupby(df_base["f_lteor"].dt.date).agg({
    #     "total_programados":"sum",
    #     "total_leidos_actual":"sum"
    # }).reset_index()

    # df_evol = df_evol.rename(columns={"f_lteor":"fecha"})

    # df_graf = df_evol.rename(columns={
    #     "total_programados": "Lecturas programadas",
    #     "total_leidos_actual": "Lecturas realizadas"
    # })

    # # import plotly.express as px

    # fig = px.line(
    #     df_graf,
    #     x="fecha",
    #     y=["Lecturas programadas", "Lecturas realizadas"],
    #     labels={
    #         "fecha": "Día de lectura",
    #         "value": "Cantidad de lecturas",
    #         "variable": "Tipo"
    #     },
    #      markers=True,
    #        title="Evolución diaria de lecturas s/fecha actual"
    # )

    # fig.update_layout(
    #     yaxis=dict(
    #         tickformat=","
    #     )
    # )

    # st.plotly_chart(fig, use_container_width=True, key="todo_actual")


























    # st.space("large") # Añade un espacio grande
    # st.subheader("Evolución diaria de lecturas")

    # df_evol = df_filtrado.groupby(df_filtrado["f_lteor"].dt.date).agg({
    #     "total_programados":"sum",
    #     "total_leidos_ftl":"sum"
    # }).reset_index()

    # df_evol = df_evol.rename(columns={"f_lteor":"fecha"})

    # df_graf = df_evol.rename(columns={
    #     "total_programados": "Lecturas programadas",
    #     "total_leidos_ftl": "Lecturas realizadas s/FTL"
    # })

    # # import plotly.express as px

    # fig = px.line(
    #     df_graf,
    #     x="fecha",
    #     y=["Lecturas programadas", "Lecturas realizadas s/FTL"],
    #     labels={
    #         "fecha": "Día de lectura",
    #         "value": "Cantidad de lecturas",
    #         "variable": "Tipo"
    #     },
    #      markers=True,
    #        title="Evolución diaria de lecturas s/FTL"
    # )

    # fig.update_layout(
    #     yaxis=dict(
    #         tickformat=","
    #     )
    # )

    # st.plotly_chart(fig, use_container_width=True, key="filtrado_ftl")





















    # st.space("large") # Añade un espacio grande
    # st.subheader("Evolución diaria de lecturas")

    # df_evol = df_filtrado.groupby(df_filtrado["f_lteor"].dt.date).agg({
    #     "total_programados":"sum",
    #     "total_leidos_actual":"sum"
    # }).reset_index()

    # df_evol = df_evol.rename(columns={"f_lteor":"fecha"})

    # df_graf = df_evol.rename(columns={
    #     "total_programados": "Lecturas programadas",
    #     "total_leidos_actual": "Lecturas realizadas"
    # })

    # # import plotly.express as px

    # fig = px.line(
    #     df_graf,
    #     x="fecha",
    #     y=["Lecturas programadas", "Lecturas realizadas"],
    #     labels={
    #         "fecha": "Día de lectura",
    #         "value": "Cantidad de lecturas",
    #         "variable": "Tipo"
    #     },
    #      markers=True,
    #        title="Evolución diaria de lecturas s/fecha actual"
        
    # )

    # fig.update_layout(
    #     yaxis=dict(
    #         tickformat=","
    #     )
    # )

    # st.plotly_chart(fig, use_container_width=True, key="filtrado_actual")













    # ----------------------------------
    # GRAFICO EVOLUCION DIARIA DE LECTURAS
    # -----------------------------------
    st.space("large") # Añade un espacio grande
    st.subheader("Evolución diaria de lecturas")

    # df_evol = df_filtrado.groupby(df_filtrado["f_lteor"].dt.date).agg({
    #     "total_programados":"sum",
    #     "total_leidos_ftl":"sum"
    # }).reset_index()
    df_evol = df_base.groupby(df_base["f_lteor"].dt.date).agg({
        "total_programados":"sum",
        "total_leidos_ftl":"sum"
    }).reset_index()

    # df_evol["fecha_str"] = df_evol["f_lteor"].dt.strftime("%d-%m")
    # df_evol["dia"] = df_evol["f_lteor"].dt.day

    df_evol = df_evol.rename(columns={"f_lteor":"fecha"})

    df_graf = df_evol.rename(columns={
        "total_programados": "Lecturas programadas",
        "total_leidos_ftl": "Lecturas realizadas s/FTL"
    })

    st.line_chart(
        df_graf.set_index("fecha")[[
            "Lecturas programadas",
            "Lecturas realizadas s/FTL"
        ]]
    )





    # df_graf = df_evol.rename(columns={
    #     "total_programados": "Lecturas programadas",
    #     "total_leidos_actual": "Lecturas realizadas"
    # })

    # fig = px.line(
    #     df_graf,
    #     x="fecha",
    #     y=["Lecturas programadas", "Lecturas realizadas"],
    #     labels={
    #         "fecha": "Día de lectura",
    #         "value": "Cantidad de lecturas",
    #         "variable": "Tipo"
    #     }
    # )

    # st.plotly_chart(fig, use_container_width=True)



    # st.line_chart(
    #     df_evol.set_index("fecha")[[
    #         "total_programados",
    #         "total_leidos_ftl"
    #     ]]
    # )
    # st.line_chart(
    #     df_evol.set_index("fecha_str")[[
    #         "total_programados",
    #         "total_leidos_ftl"
    #     ]]
    # )













    # ----------------------------------
    # GRAFICO EVOLUCION DIARIA DE LECTURAS
    # -----------------------------------
    st.space("large") # Añade un espacio grande
    st.subheader("Evolución diaria de lecturas")

    # df_evol = df_filtrado.groupby(df_filtrado["f_lteor"].dt.date).agg({
    #     "total_programados":"sum",
    #     "total_leidos_ftl":"sum"
    # }).reset_index()
    df_evol = df_base.groupby(df_base["f_lteor"].dt.date).agg({
        "total_programados":"sum",
        "total_leidos_actual":"sum"
    }).reset_index()

    # df_evol["fecha_str"] = df_evol["f_lteor"].dt.strftime("%d-%m")
    # df_evol["dia"] = df_evol["f_lteor"].dt.day

    df_evol = df_evol.rename(columns={"f_lteor":"fecha"})

    df_graf = df_evol.rename(columns={
        "total_programados": "Lecturas programadas",
        "total_leidos_actual": "Lecturas realizadas"
    })

    st.line_chart(
        df_graf.set_index("fecha")[[
            "Lecturas programadas",
            "Lecturas realizadas"
        ]]
    )


    # st.line_chart(
    #     df_evol.set_index("fecha")[[
    #         "total_programados",
    #         "total_leidos_actual"
    #     ]]
    # )
    # st.line_chart(
    #     df_evol.set_index("fecha_str")[[
    #         "total_programados",
    #         "total_leidos_ftl"
    #     ]]
    # )





















    # ----------------------------------
    # GRAFICO EVOLUCION DIARIA DE LECTURAS
    # -----------------------------------
    st.space("large") # Añade un espacio grande
    st.subheader("Evolución diaria de lecturas")

    # df_evol = df_filtrado.groupby(df_filtrado["f_lteor"].dt.date).agg({
    #     "total_programados":"sum",
    #     "total_leidos_ftl":"sum"
    # }).reset_index()
    df_evol = df_filtrado.groupby(df_filtrado["f_lteor"].dt.date).agg({
        "total_programados":"sum",
        "total_leidos_ftl":"sum"
    }).reset_index()

    # df_evol["fecha_str"] = df_evol["f_lteor"].dt.strftime("%d-%m")
    # df_evol["dia"] = df_evol["f_lteor"].dt.day

    df_evol = df_evol.rename(columns={"f_lteor":"fecha"})

    df_graf = df_evol.rename(columns={
        "total_programados": "Lecturas programadas",
        "total_leidos_ftl": "Lecturas realizadas s/FTL"
    })

    st.line_chart(
        df_graf.set_index("fecha")[[
            "Lecturas programadas",
            "Lecturas realizadas s/FTL"
        ]]
    )


    # st.line_chart(
    #     df_evol.set_index("fecha")[[
    #         "total_programados",
    #         "total_leidos_ftl"
    #     ]]
    # )
    # st.line_chart(
    #     df_evol.set_index("fecha_str")[[
    #         "total_programados",
    #         "total_leidos_ftl"
    #     ]]
    # )
















    # ----------------------------------
    # GRAFICO EVOLUCION DIARIA DE LECTURAS
    # -----------------------------------
    st.space("large") # Añade un espacio grande
    st.subheader("Evolución diaria de lecturas")

    # df_evol = df_filtrado.groupby(df_filtrado["f_lteor"].dt.date).agg({
    #     "total_programados":"sum",
    #     "total_leidos_ftl":"sum"
    # }).reset_index()
    df_evol = df_filtrado.groupby(df_filtrado["f_lteor"].dt.date).agg({
        "total_programados":"sum",
        "total_leidos_actual":"sum"
    }).reset_index()

    # df_evol["fecha_str"] = df_evol["f_lteor"].dt.strftime("%d-%m")
    # df_evol["dia"] = df_evol["f_lteor"].dt.day

    df_evol = df_evol.rename(columns={"f_lteor":"fecha"})

    df_graf = df_evol.rename(columns={
        "total_programados": "Lecturas programadas",
        "total_leidos_actual": "Lecturas realizadas"
    })

    st.line_chart(
        df_graf.set_index("fecha")[[
            "Lecturas programadas",
            "Lecturas realizadas"
        ]]
    )


    # st.line_chart(
    #     df_evol.set_index("fecha")[[
    #         "total_programados",
    #         "total_leidos_actual"
    #     ]]
    # )
    # st.line_chart(
    #     df_evol.set_index("fecha_str")[[
    #         "total_programados",
    #         "total_leidos_ftl"
    #     ]]
    # )











    st.space("large") # Añade un espacio grande
    st.subheader("Progreso del período de lectura")

    progreso_periodo = dias_transcurridos / total_dias if total_dias > 0 else 0

    st.progress(progreso_periodo)

    st.caption(
        f"{dias_transcurridos} de {total_dias} días del período transcurridos "
        f"({progreso_periodo*100:.1f}%)"
    )




    st.space("large") # Añade un espacio grande
    st.subheader("Desempeño diario")

    # df_heatmap = df_filtrado.groupby(df_filtrado["f_lteor"].dt.date).agg({
    #     "total_programados": "sum",
    #     "total_leidos_ftl": "sum"
    # }).reset_index()
    df_heatmap = df_base.groupby(df_base["f_lteor"].dt.date).agg({
        "total_programados": "sum",
        "total_leidos_ftl": "sum"
    }).reset_index()

    df_heatmap["avance_pct"] = (
        df_heatmap["total_leidos_ftl"] /
        df_heatmap["total_programados"] * 100
    )

    df_heatmap = df_heatmap.rename(columns={"f_lteor":"fecha"})


    def color_avance(val):
        if val >= 95:
            color = "#16a34a"   # verde
        elif val >= 85:
            color = "#f59e0b"   # amarillo
        else:
            color = "#ef4444"   # rojo
        return f"background-color: {color}; color: white"


    st.dataframe(
        df_heatmap.style.map(color_avance, subset=["avance_pct"])
        .format({
            "avance_pct": "{:.1f}%"
        }),
        use_container_width=True
    )




    # -----------------------------------
    # TABLA
    # -----------------------------------
    st.space("large") # Añade un espacio grande
    st.subheader("Datos filtrados s/ plazos reglamentarios + atraso")
    st.dataframe(df_filtrado, use_container_width=True)

    st.space("large") # Añade un espacio grande
    st.subheader("Datos filtrados s/ mes y tarifa")
    st.dataframe(df_base, use_container_width=True)

    st.space("large") # Añade un espacio grande
    st.subheader("Todos los datos")
    st.dataframe(df, use_container_width=True)




