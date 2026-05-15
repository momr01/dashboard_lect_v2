import streamlit as st
from streamlit_card import card
import pandas as pd
from datetime import datetime
import logging
# import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
from graficos import graf_ev_lect_atraso_ritmo, graf_ev_lect, graf_proyeccion_atraso
from secciones.page_atraso import page_atraso
from secciones.page_avance import page_avance
from secciones.page_pend import page_pend
from secciones.page_plazos import page_plazos
from secciones.page_test import page_test
from secciones.page_anomalias import page_anomalias
from reportes.reportes import generar_pdf

# -----------------------------------
# CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Dashboard Lectura",
    layout="wide",
    page_icon="📊"
)

# st.markdown("""
# <style>

# .kpi-container {
#     position: relative;
#     width: 100%;
#     height: 130px;
#     margin: 10px 0;
# }

# .kpi-card {
#     position: absolute;
#     inset: 0;
#     border-radius: 16px;
#     padding: 20px;
#     background: white;
#     border: 2px solid;
#     box-shadow: 0 6px 18px rgba(0,0,0,0.08);
#     display: flex;
#     flex-direction: column;
#     justify-content: space-between;
#     transition: all 0.2s ease;
# }

# .kpi-card:hover {
#     transform: translateY(-4px);
#     box-shadow: 0 12px 28px rgba(0,0,0,0.15);
# }

# .kpi-header {
#     display: flex;
#     justify-content: space-between;
#     align-items: center;
# }

# .kpi-title {
#     font-size: 13px;
#     color: #6b7280;
#     font-weight: 500;
# }

# .kpi-icon {
#     font-size: 20px;
# }

# .kpi-value {
#     font-size: 38px;
#     font-weight: 800;
# }

# /* botón invisible encima */
# .kpi-btn button {
#     position: absolute;
#     inset: 0;
#     opacity: 0;
#     cursor: pointer;
# }

# </style>
# """, unsafe_allow_html=True)


############################################################################
#ESTILOS DE BOTON VOLVER

st.markdown("""
<style>

/* TARGET REAL DE LOS BOTONES */
div[data-testid="stButton"] > button {
    /*height: 180px;*/
    border-radius: 16px;
    /*border: 2px solid #ddd;*/
    background: black;
    font-size: 12px;
    font-weight: 500;
    white-space: pre-line;
    transition: all 0.2s ease;
    color: white;
            

      display: flex;
    flex-direction: column;
    justify-content: center;
          

   
}
            
   

/* Hover */
div[data-testid="stButton"] > button:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    color: black;
}

/* Distribución vertical */
div[data-testid="stButton"] > button {
   /* display: flex;*/
    /*flex-direction: column;*/
    /*justify-content: center;
    align-items: center;*/
}
            
            div[data-testid="column"] div.stButton > button span {
    font-size: 22px;
    font-weight: 600;
}

/* COLORES POR COLUMNA (IMPORTANTE: usar nth-child) */
/*div[data-testid="column"]:nth-child(1) div[data-testid="stButton"] > button {
    border-color: #3b82f6;
    color: #3b82f6;
}

div[data-testid="column"]:nth-child(2) div[data-testid="stButton"] > button {
    border-color: #22c55e;
    color: #22c55e;
}*/

/*div[data-testid="column"]:nth-child(3) div[data-testid="stButton"] > button {
    border-color: #f59e0b;
    color: #f59e0b;
}*/
            


/* CONTENEDOR DEL MODAL */
div[data-testid="stDialog"] div[role="dialog"] {
    width: 90vw !important;
    max-width: 90vw !important;
}

/* CONTENIDO SCROLLEABLE */
div[data-testid="stDialog"] div[role="dialog"] > div {
    /*max-height: 85vh;*/
    overflow-y: auto;
    padding-right: 10px;
}

/* evita ese fondo raro abajo */
div[data-testid="stDialog"] {
    background: rgba(0,0,0,0.4);
}
            
            div[data-testid="stButton"] > button div {
            padding: 0;
            /*border: 1px solid red;*/
            }
            
div[data-testid="stButton"] > button p {
    /*border: 1px solid black;*/
    /*width: 200px;*/
            padding: 0;
    /*width: 400px !important;*/
    margin: 0;              /* 🔥 elimina espacio extra */
    line-height: 1.2;
    text-align: center;
    font-size: 15px;
    font-weight: 800;
            
    white-space: pre-line;     /* mantiene el salto del \n */
    word-break: keep-all;      /* 🔥 NO corta números */
            /*  width: 100% !important;  */          /* ✅ ahora sí funciona */
            
}


            
div[data-testid="stButton"] > button * {
    font-size: 12px !important;
    font-weight: 600 !important;
    /*line-height: 1.3;*/
           
}
            

            div[data-testid="stButton"] > button p::first-line {
   
    font-size: 18px;
    
}
            

  
            

</style>
""", unsafe_allow_html=True)

# st.markdown("""
# <style>

# .kpi-card{
#     //background: linear-gradient(145deg,#111827,#1f2937);
#     //background: linear-gradient(145deg,#31405E,#445069);
#     border-radius:14px;
#     padding:32px;
#     text-align:center;
#     border:2px solid;
#     box-shadow:0 4px 14px rgba(0,0,0,0.35);
#     transition:0.2s;
#     margin: 20px 0;
# }

# .kpi-card:hover{
#     background: red;
#     transform:translateY(-4px);
#     box-shadow:0 10px 22px rgba(0,0,0,0.45);
# }

# .kpi-title{
#     font-size:24px;
#     //color:#9ca3af;
#     //color: white;
#     margin-bottom:6px;
#     font-weight: bold;
# }

# .kpi-value{
#     font-size:54px;
#     font-weight:700;
# }

# .kpi-sub{
#     font-size:13px;
#     //color:#9ca3af;
#     color: black;
#     margin-top:6px;
# }
            

# /*div[data-testid="stButton"] button {
#     background: transparent;
#     border: none;
#     height: 100%;
# }*/

# /* CONTENEDOR DEL MODAL */
# div[data-testid="stDialog"] div[role="dialog"] {
#     width: 90vw !important;
#     max-width: 90vw !important;
# }

# /* CONTENIDO SCROLLEABLE */
# div[data-testid="stDialog"] div[role="dialog"] > div {
#     max-height: 85vh;
#     overflow-y: auto;
#     padding-right: 10px;
# }

# /* evita ese fondo raro abajo */
# div[data-testid="stDialog"] {
#     background: rgba(0,0,0,0.4);
# }
            

            
            
# /* Botones KPI */
# div[data-testid="column"] button {
#     height: 120px;
#     border-radius: 16px;
#     border: 2px solid #ddd;
#     background: white;
#     font-size: 16px;
#     font-weight: 500;
#     white-space: pre-line; /* 👈 permite \n */
#     transition: all 0.2s ease;

# }

# /* Hover */
# div[data-testid="column"] button:hover {
#     transform: translateY(-4px);
#     box-shadow: 0 10px 25px rgba(0,0,0,0.1);
# }

# /* Colores específicos por columna */
# div[data-testid="column"]:nth-of-type(1) button {
#     border-color: #3b82f6;
#     color: #3b82f6;
# }

# div[data-testid="column"]:nth-of-type(2) button {
#     border-color: #22c55e;
#     color: #22c55e;
# }

# div[data-testid="column"]:nth-of-type(3) button {
#     border-color: #f59e0b;
#     color: #f59e0b;
# }

# /* Tamaño del número (segunda línea) */
# div[data-testid="column"] button br + span {
#     font-size: 18px;
#     font-weight: bold;
# }
            
#             button {
#     display: flex;
#     flex-direction: column;
#     justify-content: center;
#     align-items: center;
# }

# </style>
# """, unsafe_allow_html=True)




def kpi_visual(titulo, valor, color, sub=""):
    
    st.markdown(
        f"""
        <div class="kpi-card" style="border-color:{color}">
            <div class="kpi-title">{titulo}</div>
            <div class="kpi-value" style="color:{color}">
                {valor}
            </div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True
    )



def kpi_clickable(titulo, valor, color, on_click, key, sub=""):

    container = st.container()

    with container:
        kpi_visual(
            titulo,
            valor,
            color,
            sub
        )

        clicked = st.button(
            " ",
            key=key,
            use_container_width=True
        )

    if clicked:
        on_click()



def kpi_clickable5(titulo, valor, color, on_click, key, sub=""):

    st.markdown(f"""
    <style>
    div[data-testid="stButton"][data-key="{key}"] button {{
        width:100%;
        border-radius:14px;
        padding:32px;
        border:2px solid {color};
        background:transparent;
        box-shadow:0 4px 14px rgba(0,0,0,0.35);
        transition:0.2s;
    }}

    div[data-testid="stButton"][data-key="{key}"] button:hover {{
        transform:translateY(-4px);
        box-shadow:0 10px 22px rgba(0,0,0,0.45);
    }}

    div[data-testid="stButton"][data-key="{key}"] button p {{
        margin:0;
    }}
    </style>
    """, unsafe_allow_html=True)

    label = f"""
    <div>
        <div style="font-size:24px;font-weight:bold;margin-bottom:6px;">
            {titulo}
        </div>

        <div style="font-size:54px;font-weight:700;color:{color};">
            {valor}
        </div>

        <div style="font-size:13px;margin-top:6px;">
            {sub}
        </div>
    </div>
    """

    if st.button(label, key=key, use_container_width=True):
        on_click()


def kpi_clickable4(titulo, valor, color, on_click, key, sub=""):

    st.markdown("""
    <style>
    .kpi-wrapper{
        position:relative;
    }

    .kpi-wrapper button{
        position:absolute;
        top:0;
        left:0;
        width:100%;
        height:100%;
        opacity:0;
        z-index:10;
        cursor:pointer;
    }

    .kpi-wrapper:hover{
        transform:scale(1.02);
        transition:0.15s;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="kpi-wrapper">', unsafe_allow_html=True)

    if st.button("", key=key, use_container_width=True):
        on_click()

    kpi_visual(
        titulo,
        valor,
        color,
        sub
    )

    st.markdown('</div>', unsafe_allow_html=True)


def kpi_clickable2(titulo, valor, color, on_click, key):

    st.markdown("""
    <style>
    .kpi-clickable {
        position: relative;
        cursor: pointer;
    }

    .kpi-clickable:hover {
        transform: scale(1.02);
        transition: 0.15s;
    }

    .kpi-clickable button {
        position:absolute;
        top:0;
        left:0;
        width:100%;
        height:100%;
        opacity:0;
        cursor:pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="kpi-clickable">', unsafe_allow_html=True)

    if st.button("", key=key, use_container_width=True):
        on_click()

    kpi_visual(
        titulo,
        valor,
        color
    )

    st.markdown('</div>', unsafe_allow_html=True)





def kpi_clickable3(titulo, valor, color, on_click, key):

    kpi_html = f"""
    <div style="
        padding:20px;
        border-radius:12px;
        background-color:#111827;
        border-left:6px solid {color};
        text-align:center;
    ">
        <div style="
            font-size:14px;
            color:#9ca3af;
            font-weight:600;
        ">
            {titulo}
        </div>

        <div style="
            font-size:32px;
            font-weight:700;
            color:{color};
        ">
            {valor}
        </div>
    </div>
    """

    if st.button("", key=key, use_container_width=True):
        on_click()

    st.markdown(
        f"""
        <style>
        div[data-testid="stButton"][key="{key}"] button {{
            background:transparent;
            border:none;
            padding:0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(kpi_html, unsafe_allow_html=True)


st.title("📊 Dashboard de Lecturas")

# -----------------------------------
# CARGA CSV
# -----------------------------------
# uploaded_file = st.sidebar.file_uploader(
#     "Subir archivo CSV",
#     type=["csv"]
# )

# if uploaded_file is None:
#     st.info("⬅️ Subí un archivo CSV para comenzar")
#     st.stop()

# # -----------------------------------
# # LECTURA SEGURA
# # -----------------------------------
# def leer_csv_seguro(file):
#     encodings = ["utf-8", "latin1", "cp1252", "utf-16"]

#     for enc in encodings:
#         try:
#             file.seek(0)
#             return pd.read_csv(file, encoding=enc, sep=None, engine="python")
#         except:
#             continue

#     raise Exception("No se pudo leer el archivo con codificaciones comunes")


def cargar_csv_universal(file):

    encodings = [
        "utf-8",
        "utf-8-sig",
        "utf-16",
        "latin1",
        "cp1252"
    ]

    separadores = [",", ";", "\t", "|"]

    for enc in encodings:
        for sep in separadores:
            try:
                file.seek(0)
                df = pd.read_csv(
                    file,
                    encoding=enc,
                    sep=sep,
                    engine="python"
                )

                # validar que tenga más de una columna
                if len(df.columns) > 1:
                    
                    # limpiar columnas
                    df.columns = (
                        df.columns
                        .str.strip()
                        .str.lower()
                        .str.replace("\ufeff", "", regex=False)
                    )

                    return df

            except:
                continue

    raise Exception("No se pudo interpretar el archivo CSV")
# df = leer_csv_seguro(uploaded_file)

# df.columns = df.columns.str.lower()
# df = leer_csv_seguro(uploaded_file)


# linea correctaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
# df = cargar_csv_universal(uploaded_file)


url_all = "https://raw.githubusercontent.com/momr01/csv_files/refs/heads/main/data/all.csv"

@st.cache_data
def cargar_datos(url_file):
    # encodings = ["utf-8", "utf-8-sig", "latin1", "cp1252"]
    encodings = [
        "utf-8",
        "utf-8-sig",
        "utf-16",
        "latin1",
        "cp1252"
    ]
    
    separadores = [",", ";", "\t", "|"]

    for enc in encodings:
        for sep in separadores:
            try:
                df = pd.read_csv(url_file, encoding=enc, sep=",",
                                 engine="python",
    quotechar='"',
    skipinitialspace=True,
    on_bad_lines="warn"
                                 )
                
                df.columns = (
                    df.columns
                    .str.strip()
                    .str.lower()
                    .str.replace("\ufeff", "", regex=False)
                )

                return df
            except:
                continue

    raise Exception("No se pudo leer el CSV desde GitHub")




@st.cache_data
def cargar_datos_tpl(url_file):

    encodings = ["utf-8-sig", "utf-8", "latin1", "cp1252"]
    separadores = [",", ";", "\t", "|"]

    for enc in encodings:
        for sep in separadores:
            try:
                df = pd.read_csv(
                    url_file,
                    encoding=enc,
                    sep=sep,
                    engine="python",
                    quotechar='"',
                    skipinitialspace=True,
                    on_bad_lines="warn"
                )

                # limpiar columnas
                df.columns = (
                    df.columns
                    .str.strip()
                    .str.lower()
                    .str.replace("\ufeff", "", regex=False)
                )

                columnas_esperadas = [
                    "f_actual","tarifa","cod_unicom","ruta","num_itin",
                    "ciclo","f_lteor","anio_ciclo","nl_gen","est_itin",
                    "desc_est","cantidad","leidos","faltantes","anomalias",
                    "prop_anomalias","demora_dias_corridos",
                    "demora_hab_sin_feriados","cod_contratista","contratista"
                ]

                # -----------------------------------
                # 🧠 DETECTAR HEADER CORRIDO
                # -----------------------------------
                match = sum(col in df.columns for col in columnas_esperadas)

                if match < len(columnas_esperadas) * 0.7:
                    # ❌ header sospechoso
                    st.warning("⚠️ Header desalineado detectado. Intentando corregir automáticamente...")

                    # intentar usar primera fila como header
                    df_alt = pd.read_csv(
                        url_file,
                        encoding=enc,
                        sep=sep,
                        engine="python",
                        quotechar='"',
                        skipinitialspace=True,
                        header=None,
                        on_bad_lines="skip"
                    )

                    # usar primera fila como columnas
                    df_alt.columns = (
                        df_alt.iloc[0]
                        .astype(str)
                        .str.strip()
                        .str.lower()
                        .str.replace("\ufeff", "", regex=False)
                    )

                    df_alt = df_alt[1:].reset_index(drop=True)

                    # validar si ahora mejora
                    match_alt = sum(col in df_alt.columns for col in columnas_esperadas)

                    if match_alt > match:
                        st.success("✅ Header corregido automáticamente")
                        return df_alt

                # -----------------------------------
                # VALIDACIONES GENERALES
                # -----------------------------------
                if len(df.columns) < 5:
                    continue

                if df.isnull().mean().mean() > 0.4:
                    continue

                return df

            except:
                continue

    st.error("❌ No se pudo interpretar el archivo correctamente")
    return None





import pandas as pd
import streamlit as st
import requests

@st.cache_data
def cargar_csv_ultra(url):

    response = requests.get(url)
    lines = response.text.splitlines()

    filas = [line.split(",") for line in lines]

    # detectar máximo número de columnas
    max_cols = max(len(f) for f in filas)

    # corregir filas cortas o largas
    filas_fix = []
    for f in filas:
        if len(f) < max_cols:
            f = f + [""] * (max_cols - len(f))
        elif len(f) > max_cols:
            f = f[:max_cols]
        filas_fix.append(f)

    # armar DataFrame
    df = pd.DataFrame(filas_fix[1:], columns=filas_fix[0])

    # limpiar columnas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace("\ufeff", "", regex=False)
    )

    # limpiar espacios en valores
    # df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # -----------------------------------
    # 🚨 DETECTAR PROBLEMAS
    # -----------------------------------
    # if "" in df.columns:
    #     st.warning("⚠️ Se detectaron columnas vacías (posible desalineación corregida)")

    # if df.isnull().mean().mean() > 0.2:
    #     st.warning("⚠️ Muchos valores nulos detectados. CSV inconsistente")

    # st.success("✅ Archivo cargado y corregido automáticamente")

    return df



df = cargar_datos(url_all)
# df = cargar_csv_universal(url)

# limpiar nombres de columnas
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)


url_tpl = "https://raw.githubusercontent.com/momr01/csv_files/refs/heads/main/data/tpl.csv"

##### ARCHIVO TPL
tpl = cargar_csv_ultra(url_tpl)

# tpl.columns = (
#     tpl.columns
#     .str.strip()
#     .str.lower()
# )

# tpl["f_lteor"] = pd.to_datetime(
#     tpl["f_lteor"],
#     format="%d/%m/%Y %H:%M:%S",
#     errors="coerce"
# )

# tpl["f_actual"] = pd.to_datetime(
#     tpl["f_actual"],
#     format="%d/%m/%Y %H:%M:%S",
#     errors="coerce"
# )


url_real_vs_prog = "https://raw.githubusercontent.com/momr01/csv_files/refs/heads/main/data/cuadro_resumen.csv"

##### ARCHIVO real vs programado de jorge
realvsprog = cargar_csv_ultra(url_real_vs_prog)
# st.write("Columnas detectadas:", df.columns)

# -----------------------------------
# CONVERTIR FECHA
# -----------------------------------
df["f_lteor"] = pd.to_datetime(
    df["f_lteor"],
    format="%d/%m/%Y %H:%M:%S",
    errors="coerce"
)



# -----------------------------------
# FILTROS ADICIONALES
# -----------------------------------

st.sidebar.subheader("Filtros adicionales")

# FILTRO MES
if "mes" in df.columns:
    meses = sorted(df["mes"].dropna().unique())

    meses_seleccionados = st.sidebar.multiselect(
        "Filtrar por mes",
        meses,
        default=meses
    )
else:
    meses_seleccionados = None


# FILTRO TARIFA
if "tarifa" in df.columns:
    tarifas = sorted(df["tarifa"].dropna().unique())

    tarifas_seleccionadas = st.sidebar.multiselect(
        "Filtrar por tarifa",
        tarifas,
        default=tarifas
    )
else:
    tarifas_seleccionadas = None




# -----------------------------------
# FILTRO DE FECHAS
# -----------------------------------

# st.sidebar.subheader("Filtro de fechas")
st.sidebar.subheader("Filtro para plazos reglamentarios + atraso")

fecha_min = df["f_lteor"].min()
fecha_max = df["f_lteor"].max()

fecha_inicio, fecha_fin = st.sidebar.date_input(
    "Rango de fechas",
    [fecha_min, fecha_max],
)

df_rango = df[
    (df["f_lteor"] >= pd.to_datetime(fecha_inicio)) &
    (df["f_lteor"] <= pd.to_datetime(fecha_fin))
]


df_filtrado = df_rango.copy()

# aplicar filtro mes
if meses_seleccionados is not None:
    df_filtrado = df_filtrado[df_filtrado["mes"].isin(meses_seleccionados)]

# aplicar filtro tarifa
if tarifas_seleccionadas is not None:
    df_filtrado = df_filtrado[df_filtrado["tarifa"].isin(tarifas_seleccionadas)]






# -----------------------------------
# NUEVO FILTRO: EXCLUIR DIAS
# -----------------------------------

# dias_disponibles = sorted(df_rango["f_lteor"].dt.date.unique())

# dias_seleccionados = st.sidebar.multiselect(
#     "Excluir días específicos",
#     dias_disponibles,
#     default=[]
# )

# df_filtrado = df_rango[
#     ~df_rango["f_lteor"].dt.date.isin(dias_seleccionados)
# ]



# df_filtrado = df_rango


df_base = df.copy()

# filtro mes
if meses_seleccionados:
    df_base = df_base[df_base["mes"].isin(meses_seleccionados)]

# filtro tarifa
if tarifas_seleccionadas:
    df_base = df_base[df_base["tarifa"].isin(tarifas_seleccionadas)]


 # -----------------------------
    # FILTRO PARA DESELECCIONAR FILAS
    # -----------------------------
# st.subheader("Deseleccionar filas manualmente")

# df_filtrado = df_filtrado.reset_index(drop=True)

# filas_excluir = st.multiselect(
#         "Seleccionar filas a excluir",
#         df_filtrado.index.tolist()
#     )

# if filas_excluir:
#         df_filtrado = df_filtrado.drop(filas_excluir)



# -----------------------------
# FILTRO PARA SELECCIONAR FILAS A CONSIDERAR
# -----------------------------
# st.subheader("Seleccionar filas a considerar")

# df_filtrado_regl = df_filtrado.reset_index(drop=True)

# # crear etiqueta visual para cada fila
# df_filtrado_regl["fila_label"] = (
#     "Fila "
#     + df_filtrado_regl.index.astype(str)
#     + " | "
#     + df_filtrado_regl["f_lteor"].astype(str)
# )

# opciones_filas = df_filtrado_regl["fila_label"].tolist()

# # checkbox para seleccionar todo
# seleccionar_todo = st.checkbox("Seleccionar todas las filas", value=True)

# if seleccionar_todo:
#     filas_seleccionadas = opciones_filas
# else:
#     filas_seleccionadas = st.multiselect(
#         "Seleccionar filas",
#         opciones_filas
#     )

# # filtrar dataframe
# df_filtrado_regl = df_filtrado_regl[
#     df_filtrado_regl["fila_label"].isin(filas_seleccionadas)
# ]

# # eliminar columna auxiliar
# df_filtrado_regl = df_filtrado_regl.drop(columns=["fila_label"])


# -----------------------------------
# CALCULO KPIs
# -----------------------------------

# total_programados = df_filtrado["total_programados"].sum()
# total_leidos_ftl = df_filtrado["total_leidos_ftl"].sum()
# total_programados = df["total_programados"].sum()
# total_leidos_ftl = df["total_leidos_ftl"].sum()
total_programados = df_base["total_programados"].sum()
total_leidos_ftl = df_base["total_leidos_ftl"].sum()

lecturas_pendientes = total_programados - total_leidos_ftl

# # KPI 1
# kpi_atraso = 1.4
# KPI 1 — ATRASO EN DÍAS

# agrupamos por día
df_dias = df_filtrado.groupby("f_lteor").agg({
    "total_programados": "sum",
    "total_leidos_ftl": "sum"
}).reset_index()

# calculamos diferencia diaria
df_dias["pendiente"] = df_dias["total_programados"] - df_dias["total_leidos_ftl"]

# solo consideramos pendientes positivos
pendiente_total = df_dias[df_dias["pendiente"] > 0]["pendiente"].sum()

# promedio diario programado
promedio_diario_programado = df_dias["total_programados"].mean()

# atraso en días
kpi_atraso = (
    pendiente_total / promedio_diario_programado
    if promedio_diario_programado > 0 else 0
)

kpi_atraso = round(kpi_atraso, 2)



if kpi_atraso <= 1:
    estado = "NORMAL"
    color = "#16a34a"
    emoji = "🟢"

elif kpi_atraso <= 2:
    estado = "RIESGO"
    color = "#f59e0b"
    emoji = "🟡"

else:
    estado = "CRÍTICO"
    color = "#ef4444"
    emoji = "🔴"





# KPI 1, version 2
df_dias = df_filtrado.groupby("f_lteor").agg({
    "total_programados": "sum",
    "total_leidos_ftl": "sum"
}).reset_index()

promedio_dia = df_dias["total_programados"].mean()

df_dias["gap_dias"] = (
    (df_dias["total_leidos_ftl"] - df_dias["total_programados"])
    / promedio_dia
)

kpi_atraso2 = round(max(0, -df_dias["gap_dias"].sum()), 2)





# KPI 2
kpi_reglamentarios = df_filtrado["reglamentarios"].mean()
# kpi_reglamentarios = df_filtrado_regl["reglamentarios"].mean()

# KPI 3
avance_descarga = (total_leidos_ftl / total_programados * 100) if total_programados > 0 else 0

# KPI 4
porcentaje_pendientes = (lecturas_pendientes / total_programados * 100) if total_programados > 0 else 0

# KPI 5
lecturas_descargadas = total_leidos_ftl

# KPI 6
lecturas_pendientes_total = lecturas_pendientes

# KPI 7
# total_dias = df["f_lteor"].nunique()
# dias_filtrados = df_filtrado["f_lteor"].nunique()

# dias_restantes = total_dias - dias_filtrados
# total de dias posibles en el dataset
total_dias = df_base["f_lteor"].dt.date.nunique()

# primer día del dataset (registro 0)
# primer_dia = df["f_lteor"].min().date()

# # día actual
# hoy = datetime.today().date()

# # días transcurridos desde el primer registro hasta hoy
# dias_transcurridos = (hoy - primer_dia).days + 1


hoy = datetime.today().date()

df_base["fecha"] = df_base["f_lteor"].dt.date

primer_dia = df_base["fecha"].min()

# fecha_cercana = df[df["fecha"] <= hoy]["fecha"].max()
fecha_cercana = df_base[df_base["fecha"] < hoy]["fecha"].max()

dias_transcurridos = df_base[
    (df_base["fecha"] >= primer_dia) &
    (df_base["fecha"] <= fecha_cercana)
]["fecha"].nunique()

# días restantes del período
dias_restantes = total_dias - dias_transcurridos

promedio_requerido = (
    lecturas_pendientes_total / dias_restantes
    if dias_restantes > 0 else 0
)

# st.header(f"total dias:  {total_dias}")
# st.header(f"dias transcurridos:  {dias_transcurridos}")
# st.header(f"dias restantes:  {dias_restantes}")

# st.space("medium") # Añade un espacio grande
# st.info(f"Total de días: {total_dias}")
# st.info(f"Días transcurridos: {dias_transcurridos}")
# st.info(f"Días restantes: {dias_restantes}")
# st.space("medium") # Añade un espacio grande
# st.success("Esto es un mensaje de éxito.")
# st.warning("Esto es una advertencia.")
# st.error("Esto es un mensaje de error.")


# atraso diario en días
# df_dias["atraso_dias"] = (
#     (df_dias["total_programados"] - df_dias["total_leidos_ftl"])
#     / promedio_diario_programado
# )

# df_dias["atraso_dias"] = df_dias["atraso_dias"].clip(lower=0)


# st.sidebar.subheader("Filtro de atraso")

# rango_atraso = st.sidebar.slider(
#     "Rango de atraso (días)",
#     0.0,
#     float(df_dias["atraso_dias"].max()),
#     (0.0, float(df_dias["atraso_dias"].max())),
#     step=0.1
# )


# df_dias_filtrado = df_dias[
#     (df_dias["atraso_dias"] >= rango_atraso[0]) &
#     (df_dias["atraso_dias"] <= rango_atraso[1])
# ]











#st.space("large") # Añade un espacio grande



# st.subheader("Indicador de atraso operativo")

# fig = go.Figure(go.Indicator(
#     mode="gauge+number",
#     value=kpi_atraso,
#     title={'text': "Atraso (días)"},
    
#     gauge={
#         'axis': {'range': [0, 5]},
        
#         'bar': {'color': "black"},
        
#         'steps': [
#             {'range': [0, 1], 'color': "#16a34a"},   # verde
#             {'range': [1, 2], 'color': "#f59e0b"},   # amarillo
#             {'range': [2, 5], 'color': "#ef4444"}    # rojo
#         ],
        
#         'threshold': {
#             'line': {'color': "black", 'width': 4},
#             'thickness': 0.75,
#             'value': kpi_atraso
#         }
#     }
# ))

# st.plotly_chart(fig, use_container_width=True)

# max_atraso = total_programados / promedio_diario_programado















#st.space("large") # Añade un espacio grande

# -----------------------------------
# MOSTRAR KPIs
# -----------------------------------

# col1, col2, col3, col4 = st.columns(4)

# col1.metric(
#     "ATRASO",
#     f"{kpi_atraso}"
# )

# col2.metric(
#     "PLAZOS REGLAMENTARIOS",
#     f"{kpi_reglamentarios:.2f}%"
# )

# col3.metric(
#     "AVANCE DE DESCARGA",
#     f"{avance_descarga:.2f}%"
# )

# col4.metric(
#     "% LECTURAS PENDIENTES",
#     f"{porcentaje_pendientes:.2f}%"
# )


# if "ver_detalle_atraso" not in st.session_state:
#     st.session_state.ver_detalle_atraso = False






# if "dialog_open" not in st.session_state:
#     st.session_state.dialog_open = None


@st.dialog("Detalle KPI")
def mostrar_dialog():

    tipo = st.session_state.dialog_open

    if tipo == "atraso":
        st.subheader("Evolución del atraso")

        fig = px.line(df_dias, x="f_lteor", y="gap_dias")
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df_dias, use_container_width=True)

    elif tipo == "avance":
        st.subheader("Avance de descarga")

        fig = px.line(df_dias, x="f_lteor", y="gap_dias")
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df_dias, use_container_width=True)

    elif tipo == "reglamentarios":
        st.subheader("Plazos reglamentarios")
        st.write("Acá ponés lo que quieras")

    elif tipo == "pendientes":
        st.subheader("Lecturas pendientes")
        st.write("Otro contenido")


@st.dialog("Detalle de atraso")
def mostrar_detalle_atraso(texto):

    if texto == "atraso":
        st.subheader( "Evolución del atraso")
    else:
         st.subheader( "Otrooooooo")

    # st.subheader("Detalle por día")

    # container_tabla = st.container()

    # with container_tabla:
    #     st.dataframe(
    #         df_dias,
    #         use_container_width=True,
    #         height=400
    #     )

    fig = px.line(df_dias, x="f_lteor", y="gap_dias")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detalle por día")
    st.dataframe(df_dias, use_container_width=True)

    # st.dataframe(
    #     df_dias,
    #     use_container_width=True,
    #     height=400  # 👈 CLAVE
    # )

    # if st.button("Cerrar"):
    #     st.rerun()
    if st.button("Cerrar"):
        st.session_state.dialog_open = None
        st.rerun()




@st.dialog("Avance de Descarga")
def mostrar_avance_descarga_kpi3():

    st.subheader("Evolución del atraso")

    # st.subheader("Detalle por día")

    # container_tabla = st.container()

    # with container_tabla:
    #     st.dataframe(
    #         df_dias,
    #         use_container_width=True,
    #         height=400
    #     )

    fig = px.line(df_dias, x="f_lteor", y="gap_dias")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detalle por día")
    st.dataframe(df_dias, use_container_width=True)

    # st.dataframe(
    #     df_dias,
    #     use_container_width=True,
    #     height=400  # 👈 CLAVE
    # )

    # if st.button("Cerrar"):
    #     st.rerun()
    if st.button("Cerrar"):
        st.session_state.dialog_open = None
        st.rerun()




# if st.session_state.dialog_open == "atraso":
#     mostrar_detalle_atraso()
#     # st.session_state.dialog_open = None  # 👈 CLAVE

# elif st.session_state.dialog_open == "avance":
#     mostrar_avance_descarga_kpi3()
#     # st.session_state.dialog_open = None  # 👈 CLAVE



# if st.session_state.dialog_open is not None:
#     mostrar_dialog()





#     if st.button("Ver detalle atraso"):
#         mostrar_detalle_atraso()
    # mostrar_detalle_atraso()
    # if st.button("Ver detalle"):
    #     st.session_state.ver_detalle_atraso = True

# with col1:
#     kpi_clickable(
#         "ATRASO",
#         f"{kpi_atraso2}",
#         "#ef4444",
#         mostrar_detalle_atraso,
#         "kpi_atraso"
#     )







# with col2:
#     kpi_visual(
#         "PLAZOS REGLAMENTARIOS",
#         f"{kpi_reglamentarios:.2f}%",
#         "#3b82f6"
#     )

# with col3:
#     kpi_visual(
#         "AVANCE DE DESCARGA",
#         f"{avance_descarga:.2f}%",
#         "#22c55e"
#     )

# with col4:
#     kpi_visual(
#         "% LECTURAS PENDIENTES",
#         f"{porcentaje_pendientes:.2f}%",
#         "#f59e0b"
#     )




################### ACAAAAAAAAAAAAAAAAAAA


# st.markdown("""
# <style>
# .kpi-btn button {
#     width: 100%;
#     height: 120px;
#     border-radius: 14px;
#     border: 2px solid;
#     background: white;
#     padding: 10px;
#     text-align: center;
#     font-size: 16px;
# }

# .kpi-title {
#     font-size: 14px;
#     color: black;
# }

# .kpi-value {
#     font-size: 32px;
#     font-weight: bold;
# }
# </style>
# """, unsafe_allow_html=True)



@st.dialog("Detalle KPI")
def mostrar_dialog_nuevo():

    kpi = st.session_state.dialog_kpi

    if kpi == "avance":
        st.subheader("Avance de descarga")
        fig = px.line(df_dias, x="f_lteor", y="gap_dias")
        st.plotly_chart(fig, use_container_width=True)

    elif kpi == "reglamentarios":
        st.subheader("Plazos Reglamentarios")

    elif kpi == "pendientes":
        st.subheader("Lecturas pendientes")


def kpi_button(title, value, color, key):

    st.markdown(f"""
    <div class="kpi-btn">
        <button style="border-color:{color}">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value" style="color:{color}">{value}</div>
        </button>
    </div>
    """, unsafe_allow_html=True)

    # botón invisible real (el que sí funciona)
    if st.button("", key=key):
        st.session_state.dialog_kpi = key
















import streamlit as st
import plotly.express as px


# st.markdown("""
# <style>
# .kpi-card button {
#     width: 100%;
#     height: 120px;
#     border-radius: 16px;
#     border: 2px solid;
#     background: white;
#     padding: 15px;
#     text-align: center;
#     transition: all 0.2s ease;
#     cursor: pointer;
# }

# /* hover */
# .kpi-card button:hover {
#     transform: translateY(-4px);
#     box-shadow: 0 10px 25px rgba(0,0,0,0.1);
# }

# /* título */
# .kpi-title {
#     font-size: 14px;
#     color: #444;
#     margin-bottom: 10px;
# }

# /* valor */
# .kpi-value {
#     font-size: 34px;
#     font-weight: bold;
# }
# </style>
# """, unsafe_allow_html=True)
# st.markdown("""
# <style>

# /* Botones KPI */
# div[data-testid="column"] button {
#     height: 120px;
#     border-radius: 16px;
#     border: 2px solid #ddd;
#     background: white;
#     font-size: 16px;
#     font-weight: 500;
#     white-space: pre-line; /* 👈 permite \n */
#     transition: all 0.2s ease;
# }

# /* Hover */
# div[data-testid="column"] button:hover {
#     transform: translateY(-4px);
#     box-shadow: 0 10px 25px rgba(0,0,0,0.1);
# }

# /* Colores específicos por columna */
# div[data-testid="column"]:nth-of-type(1) button {
#     border-color: #3b82f6;
#     color: #3b82f6;
# }

# div[data-testid="column"]:nth-of-type(2) button {
#     border-color: #22c55e;
#     color: #22c55e;
# }

# div[data-testid="column"]:nth-of-type(3) button {
#     border-color: #f59e0b;
#     color: #f59e0b;
# }

# /* Tamaño del número (segunda línea) */
# div[data-testid="column"] button br + span {
#     font-size: 28px;
#     font-weight: bold;
# }
            
#             button {
#     display: flex;
#     flex-direction: column;
#     justify-content: center;
#     align-items: center;
# }

# </style>
# """, unsafe_allow_html=True)


@st.dialog("Plazos Reglamentarios")
def dialog_reglamentarios():
    st.subheader("Plazos Reglamentarios")
    st.write("Contenido...")


@st.dialog("Avance de Descarga")
def dialog_avance():
    st.subheader("Avance de descarga")

    fig = px.line(df_dias, x="f_lteor", y="gap_dias")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_dias, use_container_width=True)


@st.dialog("Lecturas Pendientes")
def dialog_pendientes():
    st.subheader("Lecturas pendientes")
    st.write("Contenido...")



# def kpi_card(title, value, color, key, on_click):

#     st.markdown(f"""
#     <div class="kpi-card">
#         <button style="border-color:{color}">
#             <div class="kpi-title">{title}</div>
#             <div class="kpi-value" style="color:{color}">
#                 {value}
#             </div>
#         </button>
#     </div>
#     """, unsafe_allow_html=True)

#     # botón invisible real (el que maneja el click)
#     if st.button("", key=key):
#         on_click()

def kpi_pro(title, value, color, icon, key, on_click):

    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card" style="border-color:{color}">
            
            <div class="kpi-header">
                <div class="kpi-title">{title}</div>
                <div class="kpi-icon">{icon}</div>
            </div>

            <div class="kpi-value" style="color:{color}">
                {value}
            </div>

        </div>
        <div class="kpi-btn">
    """, unsafe_allow_html=True)

    # 👇 ESTE ES EL CLICK REAL
    if st.button("", key=key):
        on_click()

    st.markdown("</div></div>", unsafe_allow_html=True)


valor = f"{float(str(kpi_reglamentarios).replace('%','').strip()):.2f}%"
# valor = f"{float(kpi_reglamentarios):.2f}%"
# valor = str(kpi_reglamentarios).replace("\n", "") + "%"

































#acaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa



import streamlit as st
import plotly.express as px

if "page" not in st.session_state:
    st.session_state.page = "home"

if "kpi" not in st.session_state:
    st.session_state.kpi = None




def go_to(page, kpi=None):
    st.session_state.page = page
    st.session_state.kpi = kpi
    st.rerun()

def go_home():
    st.session_state.page = "home"
    st.session_state.kpi = None
    st.rerun()


from streamlit_card import card

def kpi_card(title, value, color, key):

    clicked = card(
        key=key,
        title=title,
        text=value,
        styles={
            "card": {
                "width": "100%",
                "border": f"2px solid {color}",
                "border-radius": "14px",
                "padding": "25px",
                "text-align": "center",
                "background": "linear-gradient(#ffffff, #ffffff)",
                "box-shadow": "0 10px 25px rgba(0,0,0,0.1)",
                "transition": "0.2s",
                ":hover": {
                    "transform": "translateY(-5px)"
                }
            },
            "title": {
                "color": "#6b7280",
                "font-size": "24px",
            },
            "text": {
                "color": color,
                "font-size": "62px",
                "font-weight": "bold"
            },
            "filter": {
                "background-color": "rgba(0,0,0,0)"
            }
        }
    )

    return clicked


# def render_home():

#     st.title("Dashboard")

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         if st.button(f"PLAZOS\n{kpi_reglamentarios:.2f}%", use_container_width=True):
#             go_to("detalle", "reglamentarios")

#     with col2:
#         if st.button(f"AVANCE\n{avance_descarga:.2f}%", use_container_width=True):
#             go_to("detalle", "avance")

#     with col3:
#         if st.button(f"PEND\n{porcentaje_pendientes:.2f}%", use_container_width=True):
#             go_to("detalle", "pendientes")




# st.markdown("""
# <style>

# .kpi-card{
#     //background: linear-gradient(145deg,#111827,#1f2937);
#     //background: linear-gradient(145deg,#31405E,#445069);
#     border-radius:14px;
#     padding:32px;
#     text-align:center;
#     border:2px solid;
#     box-shadow:0 4px 14px rgba(0,0,0,0.35);
#     transition:0.2s;
#     margin: 20px 0;
# }

# .kpi-card:hover{
#     transform:translateY(-4px);
#     box-shadow:0 10px 22px rgba(0,0,0,0.45);
# }

# .kpi-title{
#     font-size:24px;
#     //color:#9ca3af;
#     //color: white;
#     margin-bottom:6px;
#     font-weight: bold;
# }

# .kpi-value{
#     font-size:54px;
#     font-weight:700;
# }

# .kpi-sub{
#     font-size:13px;
#     //color:#9ca3af;
#     color: black;
#     margin-top:6px;
# }
            

# div[data-testid="stButton"] button {
#     background: transparent;
#     border: none;
#     height: 100%;
# }

# /* CONTENEDOR DEL MODAL */
# div[data-testid="stDialog"] div[role="dialog"] {
#     width: 90vw !important;
#     max-width: 90vw !important;
# }

# /* CONTENIDO SCROLLEABLE */
# div[data-testid="stDialog"] div[role="dialog"] > div {
#     max-height: 85vh;
#     overflow-y: auto;
#     padding-right: 10px;
# }

# /* evita ese fondo raro abajo */
# div[data-testid="stDialog"] {
#     background: rgba(0,0,0,0.4);
# }
            


# </style>
# """, unsafe_allow_html=True)

# def kpi_visual(titulo, valor, color, sub=""):
    
#     st.markdown(
#         f"""
#         <div class="kpi-card" style="border-color:{color}">
#             <div class="kpi-title">{titulo}</div>
#             <div class="kpi-value" style="color:{color}">
#                 {valor}
#             </div>
#             <div class="kpi-sub">{sub}</div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# def kpi_visual(titulo, valor, color, key, sub=""):

#     clicked = st.button(
#         "",
#         key=key,
#         use_container_width=True
#     )

#     st.markdown(
#         f"""
#         <style>
#         div[data-testid="stButton"][key="{key}"] > button {{
#             position: absolute;
#             inset: 0;
#             opacity: 0;
#             z-index: 10;
#             cursor: pointer;
#         }}

#         .kpi-wrapper-{key} {{
#             position: relative;
#         }}
#         </style>

#         <div class="kpi-wrapper-{key}">
#             <div class="kpi-card" style="border-color:{color}">
#                 <div class="kpi-title">{titulo}</div>

#                 <div class="kpi-value" style="color:{color}">
#                     {valor}
#                 </div>

#                 <div class="kpi-sub">{sub}</div>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     return clicked

from streamlit_card import card


# st.markdown("""
# <style>

# div[data-testid="column"] {
#     padding-left: 0.25rem !important;
#     padding-right: 0.25rem !important;
# }

# .kpi-card{
#     min-height: 120px;
#     padding: 12px;
#     border-radius: 14px;
#     border: 2px solid;
#     background: #111827;

#     display:flex;
#     flex-direction:column;
#     justify-content:center;

#     overflow:hidden;
# }

# .kpi-title{
#     font-size: clamp(11px, 1vw, 16px);
#     font-weight:600;
#     line-height:1.2;
# }

# .kpi-value{
#     font-size: clamp(18px, 2vw, 34px);
#     font-weight:700;
#     line-height:1.1;

#     word-break: break-word;
# }

# .kpi-sub{
#     font-size: clamp(10px, 0.8vw, 14px);
# }

# </style>
# """, unsafe_allow_html=True)


st.markdown("""
<style>
.block-container{
    padding-top: 1.3rem;
    padding-left: 1rem;
    padding-right: 1rem;
}
</style>
""", unsafe_allow_html=True)

# def kpi_visual(titulo, valor, color, key, sub=""):

#     clicked = card(
#         key=key,
#         title=titulo,
#         text=valor,
#         styles={
#             "card": {
#                 "width": "100%",
#                 "border": f"2px solid {color}",
#                 "border-radius": "15px",
#                 "padding": "10px",
#             },
#             "text": {
#                 "color": color,
#                 "font-size": "28px",
#                 "font-weight": "bold",
#             },
#             "title": {
#                 "font-size": "16px",
#                 "font-weight": "600",
#             }
#         }
#     )

#     return clicked


def render_home():

    # st.title("Dashboard")

    col1, col2, col3 = st.columns(3, gap="small")

    with col1:
        if kpi_card("ATRASO", f"{kpi_atraso}", "#f01212", "k1"):
            go_to("detalle", "atraso")

    with col2:
        if kpi_card("PLAZOS REGLAMENTARIOS", f"{kpi_reglamentarios:.2f}%", "#3b82f6", "k2"):
            go_to("detalle", "reglamentarios")

    with col3:
        if kpi_card("📊 AVANCE", f"{avance_descarga:.2f}%", "#22c55e", "k3"):
            go_to("detalle", "avance")

    

    


    col4, col5, col6 = st.columns(3, gap="small")

    with col4:
        if kpi_card("% LECTURAS PENDIENTES", f"{porcentaje_pendientes:.2f}%", "#f59e0b", "k4"):
            go_to("detalle", "pendientes")

    with col5:
        if kpi_card("LECTURAS DESCARGADAS", f"{lecturas_descargadas:,.0f}", "#2ed12e", "k5"):
            go_to("detalle", "atraso")

    with col6:
        if kpi_card("LECTURAS PENDIENTES",  f"{lecturas_pendientes_total:,.0f}", "#ff1d1d", "k6"):
            go_to("detalle", "reglamentarios")

    

    
    

    col7, col8, col9 = st.columns(3)

    with col7:
        if kpi_card("PROMEDIO REQUERIDO A DESCARGAR",   f"{promedio_requerido:,.0f} / día", "#c210ee", "k7"):
            go_to("detalle", "avance")

    with col8:
        if kpi_card("ANOMALIAS PENDIENTES T2 ", "133", "#aa2f54", "k8"):
            go_to("detalle", "anomalias")

    with col9:
        if kpi_card("TEST", "prueba", "#452261", "k9"):
            go_to("detalle", "test")

    # with col10:
    #     if kpi_visual(
    #         "ATRASO",
    #         f"{kpi_atraso2}",
    #         "#ef4444",
    #         "k10"
    #     ):
    #         go_to("detalle", "test")
    # with col10:
    #     kpi_visual(
    #         "ATRASO",
    #         f"{kpi_atraso2}",
    #         "#ef4444"
    #     )

# def render_detalle():

#     # 🔙 botón volver
#     st.button("⬅ Volver", on_click=go_home)

#     # título dinámico
#     if st.session_state.kpi == "reglamentarios":
#         st.title("Plazos Reglamentarios")

#     elif st.session_state.kpi == "avance":
#         st.title("Avance de Descarga")

#     elif st.session_state.kpi == "pendientes":
#         st.title("Lecturas Pendientes")

#     # 📊 gráfico
#     fig = px.line(df_dias, x="f_lteor", y="gap_dias")
#     st.plotly_chart(fig, use_container_width=True)

#     # 📋 tabla
#     st.dataframe(df_dias, use_container_width=True)



def render_detalle():

    st.button("⬅ Volver", on_click=go_home)
    # back_card()

    # titles = {
    #     "reglamentarios": "Plazos Reglamentarios",
    #     "avance": "Avance de Descarga",
    #     "pendientes": "Lecturas Pendientes"
    # }

    # st.title(titles.get(st.session_state.kpi, "Detalle"))

    # fig = px.line(df_dias, x="f_lteor", y="gap_dias")
    # st.plotly_chart(fig, use_container_width=True)

    # st.dataframe(df_dias, use_container_width=True)
    if st.session_state.kpi == "reglamentarios":
        page_plazos()
     
    elif st.session_state.kpi == "atraso":
        page_atraso(color, emoji, estado, kpi_atraso, df_base, realvsprog)
       
    elif st.session_state.kpi == "avance":
        page_avance(df_filtrado)

    elif st.session_state.kpi == "pendientes":
        page_pend(tpl)

    elif st.session_state.kpi == "anomalias":
        page_anomalias()

    elif st.session_state.kpi == "test":
        page_test(df_filtrado, dias_transcurridos, total_programados, hoy,
              df_base, dias_restantes, lecturas_pendientes_total, df)






if st.session_state.page == "home":
    render_home()

elif st.session_state.page == "detalle":
    render_detalle()














# pdf = generar_pdf()

# st.download_button(
#     label="📄 Descargar Reporte",
#     data=pdf,
#     file_name="reporte_dashboard.pdf",
#     mime="application/pdf",
#     key="123456"
# )