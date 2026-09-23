import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import io
from collections import Counter
from wordcloud import WordCloud, STOPWORDS


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="WordCloud Studio",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --cream: #F7F4EE;
    --cream-dark: #EDE8DE;
    --white: #FFFDF9;
    --taupe: #B7ADA0;
    --brown: #665B50;
    --brown-dark: #403A34;
    --olive: #69715A;
    --olive-dark: #505744;
    --border: #DED8CE;
    --soft-border: #EAE5DC;
    --shadow: rgba(74, 65, 54, 0.08);
}

/* Fondo general */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(183,173,160,0.18), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(105,113,90,0.10), transparent 25%),
        var(--cream);
    color: var(--brown-dark);
    font-family: 'DM Sans', sans-serif;
}

/* Contenedor principal */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #EFEBE3;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--brown-dark);
}

/* Textos */
h1, h2, h3 {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--brown-dark) !important;
}

p, label, .stMarkdown {
    color: var(--brown);
}

/* Título principal */
.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    font-weight: 700;
    color: var(--brown-dark);
    line-height: 1.05;
    margin-bottom: 0.2rem;
}

.main-subtitle {
    font-size: 1.05rem;
    color: #81766A;
    margin-bottom: 1.8rem;
}

/* Separadores */
hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}

/* Botones */
.stButton > button {
    width: 100%;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1rem;
    background: linear-gradient(135deg, var(--olive), var(--olive-dark));
    color: white;
    font-weight: 700;
    font-family: 'DM Sans', sans-serif;
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(80,87,68,0.20);
}

/* Inputs */
.stTextArea textarea,
.stTextInput input {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--brown-dark) !important;
}

.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: var(--olive) !important;
    box-shadow: 0 0 0 1px var(--olive) !important;
}

/* Selectores */
div[data-baseweb="select"] > div {
    background: var(--white);
    border-color: var(--border);
    border-radius: 12px;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--white);
    border: 1px dashed var(--taupe);
    border-radius: 14px;
    padding: 0.5rem;
}

/* Métricas */
[data-testid="stMetric"] {
    background: var(--white);
    border: 1px solid var(--soft-border);
    border-radius: 16px;
    padding: 1rem;
    box-shadow: 0 5px 18px var(--shadow);
}

[data-testid="stMetricLabel"] {
    color: #8A8075 !important;
}

[data-testid="stMetricValue"] {
    color: var(--brown-dark) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--white);
    border-radius: 12px;
    color: var(--brown-dark);
    font-weight: 600;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

/* Download */
.stDownloadButton > button {
    width: 100%;
    background: var(--brown);
    color: white;
    border: none;
    border-radius: 11px;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background: var(--brown-dark);
    color: white;
}

/* Alertas */
div[data-testid="stAlert"] {
    border-radius: 13px;
}

/* Radio buttons */
.stRadio label {
    color: var(--brown-dark) !important;
}

/* Checkbox */
.stCheckbox label {
    color: var(--brown-dark) !important;
}

/* Slider */
.stSlider {
    color: var(--olive);
}

/* Caption */
.stCaption {
    color: #8A8075 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# STOPWORDS EN ESPAÑOL
# ============================================================

STOPWORDS_ES = {
    "de", "la", "que", "el", "en", "y", "a", "los", "del",
    "se", "las", "por", "un", "para", "con", "no", "una",
    "su", "al", "lo", "como", "más", "pero", "sus", "le",
    "ya", "o", "este", "sí", "porque", "esta", "entre",
    "cuando", "muy", "sin", "sobre", "también", "me",
    "hasta", "hay", "donde", "quien", "desde", "todo",
    "nos", "durante", "todos", "uno", "les", "ni", "contra",
    "otros", "ese", "eso", "ante", "ellos", "e", "esto",
    "mí", "antes", "algunos", "qué", "unos", "yo", "otro",
    "otras", "otra", "él", "tanto", "esa", "estos", "mucho",
    "quienes", "nada", "muchos", "cual", "poco", "ella",
    "estar", "estas", "algunas", "algo", "nosotros", "mi",
    "mis", "tú", "te", "ti", "tu", "tus", "ellas", "ellos",
    "fue", "era", "son", "es", "ser", "han", "ha", "he",
    "se", "está", "están", "estaba", "estaban"
}


# ============================================================
# PALETAS
# ============================================================

PALETAS = {

    # Originales
    "Escala de grises": [
        "#222222", "#444444", "#666666",
        "#888888", "#AAAAAA", "#CCCCCC"
    ],

    "Azul corporativo": [
        "#0B1F3A", "#123B63", "#165A8A",
        "#1D78B5", "#4599C8", "#83C0DF"
    ],

    "Verde institucional": [
        "#12372A", "#1E5631", "#2E7D4F",
        "#4E9F6A", "#75B985", "#A9D4B3"
    ],

    "Gris azulado": [
        "#263238", "#37474F", "#455A64",
        "#607D8B", "#78909C", "#B0BEC5"
    ],

    "Terracota": [
        "#542E25", "#733E31", "#95513F",
        "#B96A54", "#D28B73", "#E6B5A1"
    ],

    "Índigo profundo": [
        "#20163D", "#30215C", "#42307B",
        "#59439B", "#7764B7", "#A69BD1"
    ],

    "Monocromático negro": [
        "#111111", "#222222", "#333333",
        "#555555", "#777777", "#999999"
    ],

    "Rosado fiesta": [
        "#641C3D", "#8E2854", "#B83E6B",
        "#D75B83", "#EA86A4", "#F3B8C9"
    ],

    # Nuevas paletas neutras
    "Café & crema": [
        "#3B302A", "#59483D", "#7A6657",
        "#9B8574", "#B8A99A", "#D8CEC2", "#EFE7DE"
    ],

    "Arena": [
        "#4A4036", "#6B5B4D", "#8C7A67",
        "#A99783", "#C1B3A3", "#D9CFC3", "#EEE7DF"
    ],

    "Oliva suave": [
        "#3F4538", "#555E4A", "#69715A",
        "#7E866D", "#9DA58B", "#BDC3AA", "#D9DDCE"
    ],

    "Terracota neutro": [
        "#4A2F27", "#684138", "#865344",
        "#A96A54", "#C1846B", "#D5A18B", "#E8C7B7"
    ],

    "Moca": [
        "#2F2723", "#4A3A32", "#665047",
        "#82695D", "#9D8376", "#BCA99D", "#D9CCC4"
    ],

    "Piedra": [
        "#343434", "#4E4E4A", "#686761",
        "#828077", "#9B978B", "#B8B2A5", "#D5D0C5"
    ],

    "Azul grisáceo neutro": [
        "#28343B", "#3E4B52", "#56636A",
        "#6F7B81", "#899398", "#AAB1B3", "#D0D3D2"
    ],

    "Lavanda gris": [
        "#3D3945", "#55505F", "#6E6879",
        "#898294", "#A39BAE", "#C1BAC7", "#DED9E1"
    ],

    "Sage & cream": [
        "#3D463D", "#526053", "#687267",
        "#7E887C", "#9CA498", "#BBC0B6", "#D9DDD6"
    ]
}


# ============================================================
# FORMAS
# ============================================================

FORMAS = {
    "Rectángulo": None,
    "Círculo": "circle"
}


# ============================================================
# FUNCIONES
# ============================================================

def obtener_stopwords(idioma):
    if idioma == "Español":
        return STOPWORDS_ES
    return set(STOPWORDS)


def crear_mascara(tipo):
    if tipo == "Círculo":
        y, x = np.ogrid[-1:1:500j, -1:1:500j]
        mask = x * x + y * y <= 1
        return (mask * 255).astype(np.uint8)

    return None


def limpiar_texto(texto, stopwords, extras):
    texto = texto.lower()

    texto = re.sub(r"http\S+|www\S+", " ", texto)
    texto = re.sub(r"[^a-záéíóúüñA-ZÁÉÍÓÚÜÑ\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto)

    palabras = texto.split()

    extras_set = {
        palabra.strip().lower()
        for palabra in extras.split(",")
        if palabra.strip()
    }

    palabras_limpias = [
        palabra
        for palabra in palabras
        if palabra not in stopwords
        and palabra not in extras_set
        and len(palabra) > 2
    ]

    return " ".join(palabras_limpias)


def contar_palabras(texto):
    palabras = texto.split()
    return Counter(palabras)


def generar_wordcloud(
    texto,
    paleta,
    fondo,
    forma,
    max_words
):

    mask = crear_mascara(forma)

    wc = WordCloud(
        width=1400,
        height=800,
        background_color=fondo,
        max_words=max_words,
        mask=mask,
        collocations=False,
        color_func=None
    )

    wc.generate(texto)

    # Aplicar la paleta manualmente
    colores = paleta

    def color_func(
        word,
        font_size,
        position,
        orientation,
        random_state=None,
        **kwargs
    ):
        indice = np.random.randint(0, len(colores))
        return colores[indice]

    wc.recolor(color_func=color_func)

    return wc


def fig_a_bytes(fig):
    buffer = io.BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=200,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )

    buffer.seek(0)
    return buffer.getvalue()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("☁️ WordCloud Studio")

    st.caption("Crea nubes de palabras limpias, elegantes y personalizadas.")

    st.divider()

    st.subheader("📝 Fuente del texto")

    fuente = st.radio(
        "Selecciona una fuente",
        ["Escribir / pegar", "Subir archivo"],
        label_visibility="collapsed"
    )

    texto = ""

    if fuente == "Escribir / pegar":

        ejemplo = st.selectbox(
            "Usar un ejemplo",
            [
                "Ninguno",
                "Inteligencia Artificial",
                "Colombia",
                "Tecnología 4.0"
            ]
        )

        ejemplos = {
            "Ninguno": "",
            "Inteligencia Artificial": """
            La inteligencia artificial está transformando la educación,
            la tecnología, las empresas y la vida cotidiana.
            Los sistemas inteligentes permiten analizar información,
            automatizar procesos y crear nuevas experiencias.
            """,

            "Colombia": """
            Colombia es un país diverso con diferentes culturas,
            regiones, paisajes, tradiciones y comunidades.
            Medellín, Bogotá, Cartagena, Cali y muchas otras ciudades
            representan la diversidad cultural colombiana.
            """,

            "Tecnología 4.0": """
            La tecnología 4.0 combina inteligencia artificial,
            automatización, internet de las cosas, datos,
            robótica, innovación y transformación digital.
            """
        }

        texto = st.text_area(
            "Escribe o pega tu texto",
            value=ejemplos[ejemplo],
            height=250,
            placeholder="Escribe aquí el texto que quieres analizar..."
        )

    else:

        archivo = st.file_uploader(
            "Sube un archivo",
            type=["txt", "csv"]
        )

        if archivo is not None:

            try:

                if archivo.name.endswith(".txt"):
                    texto = archivo.read().decode("utf-8")

                else:
                    df_archivo = pd.read_csv(archivo)

                    if len(df_archivo.columns) > 0:
                        texto = " ".join(
                            df_archivo.astype(str).values.flatten()
                        )

            except Exception as e:
                st.error(f"No se pudo leer el archivo: {e}")

    st.divider()

    st.subheader("🧹 Limpieza")

    idioma = st.selectbox(
        "Idioma",
        ["Español", "Inglés"]
    )

    palabras_extra = st.text_input(
        "Palabras adicionales a excluir",
        placeholder="ejemplo, palabra, texto"
    )

    st.divider()

    st.subheader("🎨 Apariencia")

    paleta_nombre = st.selectbox(
        "Paleta de colores",
        list(PALETAS.keys()),
        index=list(PALETAS.keys()).index("Café & crema")
    )

    fondo = st.radio(
        "Fondo de la nube",
        ["Blanco", "Negro"],
        horizontal=True
    )

    fondo_color = "#FFFDF9" if fondo == "Blanco" else "#151515"

    forma = st.selectbox(
        "Forma",
        list(FORMAS.keys())
    )

    max_words = st.slider(
        "Máximo de palabras",
        min_value=20,
        max_value=300,
        value=100,
        step=10
    )

    st.divider()

    generar = st.button(
        "☁️ Generar WordCloud",
        use_container_width=True
    )


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    '<div class="main-title">WordCloud Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Transforma tus textos en visualizaciones de palabras '
    'elegantes y personalizadas.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ESTADO INICIAL
# ============================================================

if "wordcloud_generado" not in st.session_state:
    st.session_state.wordcloud_generado = False

if "texto_procesado" not in st.session_state:
    st.session_state.texto_procesado = ""

if "frecuencias" not in st.session_state:
    st.session_state.frecuencias = Counter()

if "wordcloud" not in st.session_state:
    st.session_state.wordcloud = None


# ============================================================
# GENERACIÓN
# ============================================================

if generar:

    if not texto.strip():

        st.warning(
            "⚠️ Primero escribe, pega o sube un texto para generar la nube."
        )

    else:

        with st.spinner("Analizando y creando tu nube de palabras..."):

            stopwords = obtener_stopwords(idioma)

            texto_procesado = limpiar_texto(
                texto,
                stopwords,
                palabras_extra
            )

            if not texto_procesado.strip():

                st.error(
                    "No quedaron palabras suficientes después de la limpieza."
                )

            else:

                frecuencias = contar_palabras(texto_procesado)

                nube = generar_wordcloud(
                    texto_procesado,
                    PALETAS[paleta_nombre],
                    fondo_color,
                    forma,
                    max_words
                )

                st.session_state.wordcloud_generado = True
                st.session_state.texto_procesado = texto_procesado
                st.session_state.frecuencias = frecuencias
                st.session_state.wordcloud = nube


# ============================================================
# PANTALLA DE BIENVENIDA
# ============================================================

if not st.session_state.wordcloud_generado:

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📝 Analiza")
        st.write(
            "Pega un texto o carga un archivo para comenzar."
        )

    with col2:
        st.subheader("🧹 Limpia")
        st.write(
            "Elimina palabras comunes y términos que no quieras analizar."
        )

    with col3:
        st.subheader("🎨 Personaliza")
        st.write(
            "Elige colores, forma, fondo y cantidad de palabras."
        )

    st.info(
        "💡 Consejo: utiliza textos suficientemente largos para obtener "
        "una nube de palabras más representativa."
    )


# ============================================================
# RESULTADOS
# ============================================================

if st.session_state.wordcloud_generado:

    texto_procesado = st.session_state.texto_procesado
    frecuencias = st.session_state.frecuencias
    nube = st.session_state.wordcloud

    st.divider()

    st.subheader("📊 Resumen del análisis")

    total_palabras = len(texto.split())
    palabras_unicas = len(frecuencias)
    palabra_mas_frecuente = (
        frecuencias.most_common(1)[0][0]
        if frecuencias
        else "-"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Palabras originales",
            f"{total_palabras:,}"
        )

    with col2:
        st.metric(
            "Palabras únicas",
            f"{palabras_unicas:,}"
        )

    with col3:
        st.metric(
            "Palabra principal",
            palabra_mas_frecuente
        )

    with col4:
        st.metric(
            "Palabras mostradas",
            f"{min(max_words, palabras_unicas):,}"
        )

    st.divider()

    # ========================================================
    # WORDCLOUD
    # ========================================================

    st.subheader("☁️ Tu WordCloud")

    fig, ax = plt.subplots(
        figsize=(15, 8)
    )

    ax.imshow(
        nube,
        interpolation="bilinear"
    )

    ax.axis("off")

    fig.patch.set_facecolor(fondo_color)
    ax.set_facecolor(fondo_color)

    st.pyplot(
        fig,
        use_container_width=True
    )

    png_bytes = fig_a_bytes(fig)

    plt.close(fig)

    st.download_button(
        "⬇️ Descargar WordCloud en PNG",
        data=png_bytes,
        file_name="wordcloud.png",
        mime="image/png",
        use_container_width=True
    )

    st.divider()

    # ========================================================
    # FRECUENCIAS
    # ========================================================

    st.subheader("📈 Palabras más frecuentes")

    top_20 = frecuencias.most_common(20)

    if top_20:

        freq_df = pd.DataFrame(
            top_20,
            columns=["Palabra", "Frecuencia"]
        )

        col1, col2 = st.columns([1.15, 1])

        with col1:

            st.dataframe(
                freq_df,
                use_container_width=True,
                hide_index=True
            )

        with col2:

            fig2, ax2 = plt.subplots(
                figsize=(8, 6)
            )

            palabras = [
                item[0]
                for item in reversed(top_20)
            ]

            cantidades = [
                item[1]
                for item in reversed(top_20)
            ]

            ax2.barh(
                palabras,
                cantidades
            )

            ax2.set_xlabel("Frecuencia")
            ax2.set_ylabel("")

            ax2.spines["top"].set_visible(False)
            ax2.spines["right"].set_visible(False)

            fig2.tight_layout()

            st.pyplot(
                fig2,
                use_container_width=True
            )

            plt.close(fig2)

        csv = freq_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Descargar frecuencias CSV",
            data=csv,
            file_name="frecuencias_wordcloud.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.divider()

    # ========================================================
    # TEXTO PROCESADO
    # ========================================================

    with st.expander("🔍 Ver texto procesado"):

        st.write(
            texto_procesado
        )

        st.caption(
            f"Caracteres procesados: {len(texto_procesado):,}"
        )

    st.divider()

    st.caption(
        "WordCloud Studio · Visualización de texto"
    )
