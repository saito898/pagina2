import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Mi cuento parlanchín 🧸",
    page_icon="🧸",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&display=swap');

:root {
    --rosa: #FF8FAB;
    --rosa-claro: #FFD6E0;
    --amarillo: #FFD166;
    --amarillo-claro: #FFF1B8;
    --azul: #74C0FC;
    --azul-claro: #DDF3FF;
    --morado: #B197FC;
    --morado-claro: #E9DDFF;
    --verde: #8BD3A8;
    --verde-claro: #DDF7E7;
    --blanco: #FFFFFF;
    --texto: #51465A;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #FFE6ED 0%, transparent 25%),
        radial-gradient(circle at 90% 15%, #E6F6FF 0%, transparent 25%),
        radial-gradient(circle at 50% 100%, #FFF4C7 0%, transparent 30%),
        #FFF9FC;

    font-family: 'Baloo 2', cursive;
    color: var(--texto);
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #FFF0F5 0%,
        #F2E9FF 50%,
        #E9F8FF 100%
    );

    border-right: 3px solid #FFD6E0;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #69556F !important;
    font-family: 'Baloo 2', cursive !important;
}


/* ============================================================
   TÍTULOS
   ============================================================ */

h1, h2, h3 {
    font-family: 'Baloo 2', cursive !important;
    color: #51465A !important;
}

.main-title {
    font-size: 3.8rem;
    font-weight: 800;
    color: #51465A;
    text-align: center;
    line-height: 1;
    margin-bottom: 0.3rem;
}

.main-subtitle {
    text-align: center;
    font-size: 1.3rem;
    color: #8A748F;
    margin-bottom: 1.5rem;
}


/* ============================================================
   TARJETA PRINCIPAL
   ============================================================ */

.story-card {
    background: rgba(255,255,255,0.92);
    border-radius: 30px;
    padding: 2rem;
    border: 3px solid #FFE0E8;
    box-shadow: 0 12px 35px rgba(140, 100, 130, 0.12);
    margin-bottom: 1.5rem;
}


/* ============================================================
   ÁREA DE TEXTO
   ============================================================ */

.stTextArea textarea {
    background: #FFFFFF !important;
    border: 3px solid #FFD6E0 !important;
    border-radius: 20px !important;
    color: #51465A !important;
    font-family: 'Baloo 2', cursive !important;
    font-size: 1.05rem !important;
}

.stTextArea textarea:focus {
    border-color: #FF8FAB !important;
    box-shadow: 0 0 0 3px rgba(255,143,171,0.15) !important;
}


/* ============================================================
   SELECTORES
   ============================================================ */

div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 2px solid #DCCFF2 !important;
    border-radius: 15px !important;
    color: #51465A !important;
}


/* ============================================================
   BOTONES
   ============================================================ */

.stButton > button {
    border: none;
    border-radius: 18px;
    padding: 0.8rem 1.2rem;
    font-family: 'Baloo 2', cursive;
    font-size: 1.15rem;
    font-weight: 700;
    background: linear-gradient(
        135deg,
        #FF8FAB,
        #FFB3C6
    );
    color: white;
    box-shadow: 0 7px 0 #E87595;
    transition: all 0.15s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 9px 0 #E87595;
}

.stButton > button:active {
    transform: translateY(4px);
    box-shadow: 0 3px 0 #E87595;
}


/* ============================================================
   AUDIO
   ============================================================ */

audio {
    width: 100%;
    border-radius: 15px;
}


/* ============================================================
   DOWNLOAD
   ============================================================ */

.stDownloadButton > button {
    border: none;
    border-radius: 16px;
    background: #8BD3A8;
    color: white;
    font-family: 'Baloo 2', cursive;
    font-weight: 700;
    box-shadow: 0 5px 0 #68B889;
}

.stDownloadButton > button:hover {
    background: #7BC798;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.8);
    border: 2px dashed #C9B8E8;
    border-radius: 18px;
}


/* ============================================================
   ALERTAS
   ============================================================ */

div[data-testid="stAlert"] {
    border-radius: 18px;
    font-family: 'Baloo 2', cursive;
}


/* ============================================================
   RADIO
   ============================================================ */

.stRadio label {
    color: #51465A !important;
    font-weight: 600;
}


/* ============================================================
   DIVISORES
   ============================================================ */

hr {
    border: none;
    border-top: 2px dashed #FFD6E0;
    margin: 1.5rem 0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CARPETA TEMPORAL
# ============================================================

os.makedirs("temp", exist_ok=True)


# ============================================================
# FUNCIÓN TEXT TO SPEECH
# ============================================================

def text_to_speech(text, language):

    if not text.strip():
        return None

    tts = gTTS(
        text=text,
        lang=language,
        slow=False
    )

    # Nombre seguro para el archivo
    nombre = "cuento_audio"

    archivo = f"temp/{nombre}.mp3"

    tts.save(archivo)

    return archivo


# ============================================================
# LIMPIAR ARCHIVOS ANTIGUOS
# ============================================================

def remove_files(days):

    mp3_files = glob.glob("temp/*.mp3")

    if len(mp3_files) == 0:
        return

    now = time.time()
    seconds = days * 86400

    for archivo in mp3_files:

        try:

            if os.stat(archivo).st_mtime < now - seconds:
                os.remove(archivo)

        except:
            pass


remove_files(7)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🧸 Mi cuento parlanchín")

    st.write(
        "¡Escribe una historia y deja que yo te la lea! 🌈"
    )

    st.divider()

    st.subheader("🌎 Idioma")

    idioma = st.selectbox(
        "¿En qué idioma quieres escuchar?",
        ["🇪🇸 Español", "🇺🇸 English"]
    )

    if idioma == "🇪🇸 Español":
        language_code = "es"
    else:
        language_code = "en"

    st.divider()

    st.subheader("💡 ¿Cómo funciona?")

    st.write("1️⃣ Escribe o pega tu texto.")
    st.write("2️⃣ Elige el idioma.")
    st.write("3️⃣ Presiona el botón.")
    st.write("4️⃣ ¡Escucha tu historia! 🎧")


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    '<div class="main-title">🧸 Mi cuento parlanchín</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    '✨ Escribe algo divertido y yo lo convertiré en voz ✨'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TARJETA DE TEXTO
# ============================================================

st.markdown(
    '<div class="story-card">',
    unsafe_allow_html=True
)

st.subheader("📖 ¡Escribe tu historia!")

st.write(
    "Puedes escribir un cuento, una tarea, una historia "
    "o cualquier texto que quieras escuchar."
)

texto = st.text_area(
    "Texto para escuchar",
    height=300,
    placeholder=(
        "Había una vez...\n\n"
        "Escribe o pega aquí tu texto y luego presiona "
        "el botón para escucharlo. 🌟"
    ),
    label_visibility="collapsed"
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# BOTÓN DE GENERACIÓN
# ============================================================

col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    convertir = st.button(
        "🔊 ¡Quiero escucharlo!",
        use_container_width=True
    )


# ============================================================
# GENERAR AUDIO
# ============================================================

if convertir:

    if not texto.strip():

        st.warning(
            "✏️ ¡Primero escribe algo para poder leerlo!"
        )

    else:

        with st.spinner("🪄 Preparando tu voz mágica..."):

            try:

                audio_path = text_to_speech(
                    texto,
                    language_code
                )

                with open(audio_path, "rb") as audio_file:

                    audio_bytes = audio_file.read()

                st.success(
                    "🎉 ¡Listo! Tu historia está preparada."
                )

                st.subheader("🎧 ¡Hora de escuchar!")

                st.audio(
                    audio_bytes,
                    format="audio/mp3"
                )

                st.download_button(
                    "💾 Guardar audio",
                    data=audio_bytes,
                    file_name="mi_cuento.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    f"😿 No pudimos crear el audio. Error: {e}"
                )


# ============================================================
# MENSAJE FINAL
# ============================================================

if not convertir:

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "📚 **Cuentos**\n\n"
            "Escribe tus propias historias."
        )

    with col2:
        st.info(
            "🎤 **Voz**\n\n"
            "Convierte tus palabras en audio."
        )

    with col3:
        st.info(
            "🌈 **Diversión**\n\n"
            "¡Escucha y disfruta!"
        )
