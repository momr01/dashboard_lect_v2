import streamlit as st
import pandas as pd
import plotly.express as px

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from io import BytesIO
import tempfile



# =========================
# DATOS EJEMPLO
# =========================

df = pd.DataFrame({
    "Dia": [1,2,3,4,5],
    "Programado": [100,120,150,170,200],
    "Real": [90,130,140,180,210]
})



# =========================
# GRAFICO PLOTLY
# =========================

fig = px.line(
    df,
    x="Dia",
    y=["Programado", "Real"],
    markers=True,
    title="Evolución diaria"
)



# =========================
# FUNCION PDF
# =========================

def generar_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm
    )

    styles = getSampleStyleSheet()

    elements = []



    # =========================
    # TITULO
    # =========================

    titulo = Paragraph(
        "<b>Estado actual de anomalías T2 / descarga de lecturas</b>",
        styles["Title"]
    )

    elements.append(titulo)
    elements.append(Spacer(1, 20))

    ## SECCION 1 - LECTURAS
    # titulo_lecturas = Paragraph("<b>LECTURAS</b>", styles[""])







    titulo = Paragraph(
    """
    <para align='center'>
        <u><b>EVOLUCIÓN DIARIA T1</b></u>
    </para>
    """,
    styles["Heading2"]
)

    elements.append(titulo)
    elements.append(Spacer(1, 15))




    subtitulo = Paragraph(
    """
    <u><b>Anomalías T2</b></u>
    """,
    styles["Heading3"]
)

    elements.append(subtitulo)
    elements.append(Spacer(1, 10))




    texto = Paragraph(
    """
    Actualmente se registran 130 anomalías T2 pendientes de resolución,
    acumuladas desde el 01/05/2025 hasta hoy.
    """,
    styles["BodyText"]
)

    elements.append(texto)
    elements.append(Spacer(1, 15))




    elements.append(Spacer(1, 30))
    Spacer(1, 10)
    Spacer(1, 20)
    Spacer(1, 40)


    # =========================
    # KPI TABLE
    # =========================

    kpi_data = [
        ["Indicador", "Valor"],
        ["Avance", "30%"],
        ["Pendientes", "70%"],
        ["Lecturas", "165.970"]
    ]

    kpi_table = Table(
        kpi_data,
        colWidths=[8*cm, 5*cm]
    )

    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#d9d9d9")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 10),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("BOTTOMPADDING", (0,0), (-1,0), 10),

        ("BACKGROUND", (0,1), (-1,-1), colors.white),
    ]))

    elements.append(kpi_table)
    elements.append(Spacer(1, 25))



    # =========================
    # EXPORTAR GRAFICO A PNG
    # =========================

    temp_img = tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False
    )

    fig.write_image(
        temp_img.name,
        width=1200,
        height=500
    )



    # =========================
    # INSERTAR GRAFICO
    # =========================

    grafico = Image(
        temp_img.name,
        width=17*cm,
        height=7*cm
    )

    elements.append(grafico)
    elements.append(Spacer(1, 20))



    # =========================
    # TABLA DETALLE
    # =========================

    table_data = [df.columns.tolist()] + df.values.tolist()

    detail_table = Table(
        table_data,
        repeatRows=1
    )

    detail_table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#4472C4")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),

        ("ROWBACKGROUNDS", (0,1), (-1,-1),
            [colors.white, colors.HexColor("#f2f2f2")]
        ),

    ]))

    elements.append(detail_table)





    data = [
    ["Estado", "Prom", "Avance", "% Lecturas"],
    ["NORMAL", "97%", "30%", "70%"]
]

    table = Table(data, colWidths=[100,80,80,80])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))



    # =========================
    # GENERAR PDF
    # =========================

    doc.build(elements)

    buffer.seek(0)

    return buffer



# =========================
# STREAMLIT
# =========================

# st.title("Dashboard")

# st.plotly_chart(fig, use_container_width=True)

# st.dataframe(df)



# =========================
# BOTON DESCARGA
# =========================

# pdf = generar_pdf()

# st.download_button(
#     label="📄 Descargar PDF",
#     data=pdf,
#     file_name="reporte_dashboard.pdf",
#     mime="application/pdf"
# )