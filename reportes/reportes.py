import pandas as pd
import matplotlib.pyplot as plt

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


# ==========================================
# DATOS EJEMPLO
# ==========================================

df = pd.DataFrame({
    "Dia": [1, 2, 3, 4, 5],
    "Programado": [100, 120, 150, 170, 200],
    "Real": [90, 130, 140, 180, 210]
})


# ==========================================
# GRAFICO MATPLOTLIB
# ==========================================

def generar_grafico_png(path_archivo):

    plt.figure(figsize=(12, 5))

    plt.plot(
        df["Dia"],
        df["Programado"],
        marker="o",
        linewidth=2,
        label="Programado"
    )

    plt.plot(
        df["Dia"],
        df["Real"],
        marker="o",
        linewidth=2,
        label="Real"
    )

    plt.title("Evolución diaria")
    plt.xlabel("Día")
    plt.ylabel("Cantidad")
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        path_archivo,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ==========================================
# PDF
# ==========================================

def generar_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1 * cm,
        leftMargin=1 * cm,
        topMargin=1 * cm,
        bottomMargin=1 * cm
    )

    styles = getSampleStyleSheet()

    elements = []

    # ==========================================
    # TITULO PRINCIPAL
    # ==========================================

    titulo = Paragraph(
        "<b>Estado actual de anomalías T2 / descarga de lecturas</b>",
        styles["Title"]
    )

    elements.append(titulo)
    elements.append(Spacer(1, 20))

    # ==========================================
    # TITULO CENTRADO
    # ==========================================

    titulo2 = Paragraph(
        """
        <para align='center'>
            <u><b>EVOLUCIÓN DIARIA T1</b></u>
        </para>
        """,
        styles["Heading2"]
    )

    elements.append(titulo2)
    elements.append(Spacer(1, 15))

    # ==========================================
    # SUBTITULO
    # ==========================================

    subtitulo = Paragraph(
        """
        <u><b>Anomalías T2</b></u>
        """,
        styles["Heading3"]
    )

    elements.append(subtitulo)
    elements.append(Spacer(1, 10))

    # ==========================================
    # TEXTO
    # ==========================================

    texto = Paragraph(
        """
        Actualmente se registran 130 anomalías T2 pendientes de resolución,
        acumuladas desde el 01/05/2025 hasta hoy.
        """,
        styles["BodyText"]
    )

    elements.append(texto)
    elements.append(Spacer(1, 20))

    # ==========================================
    # TABLA KPI
    # ==========================================

    kpi_data = [
        ["Indicador", "Valor"],
        ["Avance", "30%"],
        ["Pendientes", "70%"],
        ["Lecturas", "165.970"]
    ]

    kpi_table = Table(
        kpi_data,
        colWidths=[8 * cm, 5 * cm]
    )

    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9d9d9")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(kpi_table)
    elements.append(Spacer(1, 25))

    # ==========================================
    # GRAFICO
    # ==========================================

    temp_img = tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False
    )

    generar_grafico_png(temp_img.name)

    grafico = Image(
        temp_img.name,
        width=17 * cm,
        height=7 * cm
    )

    elements.append(grafico)
    elements.append(Spacer(1, 20))

    # ==========================================
    # TABLA DETALLE
    # ==========================================

    table_data = [df.columns.tolist()] + df.values.tolist()

    detail_table = Table(
        table_data,
        repeatRows=1
    )

    detail_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS",
         (0, 1),
         (-1, -1),
         [colors.white, colors.HexColor("#f2f2f2")]),
    ]))

    elements.append(detail_table)

    elements.append(Spacer(1, 20))

    # ==========================================
    # TABLA RESUMEN
    # ==========================================

    data = [
        ["Estado", "Prom", "Avance", "% Lecturas"],
        ["NORMAL", "97%", "30%", "70%"]
    ]

    table = Table(
        data,
        colWidths=[100, 80, 80, 80]
    )

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))

    elements.append(table)

    # ==========================================
    # GENERAR PDF
    # ==========================================

    doc.build(elements)

    buffer.seek(0)

    return buffer