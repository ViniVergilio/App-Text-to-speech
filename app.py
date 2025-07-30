import streamlit as st
from gtts import gTTS
import subprocess
import base64
import os

# Caminho do FFmpeg
FFMPEG_PATH = r"C:\Users\Proje\Downloads\ffmpeg-2025-07-28-git-dc8e753f32-essentials_build\bin\ffmpeg.exe"

# Configurações da página
st.set_page_config(page_title="Leitor de Texto Interativo", page_icon="🎙️", layout="centered")

# CSS com sliders sem ticks
st.markdown("""
    <style>
        body, .stApp {
            background-color: #ffffff !important;
            color: #1D3269 !important;
            font-family: 'Poppins', sans-serif;
        }

        h1, h2, h3, h4, h5, h6, p, label {
            color: #1D3269 !important;
        }

        /* Inputs e Textarea */
        textarea, .stTextArea textarea {
            background-color: #ffffff !important;
            color: #1D3269 !important;
            border: 1px solid #1D3269 !important;
            border-radius: 6px !important;
            padding: 8px !important;
            font-size: 15px !important;
        }

        /* Selectbox */
        .stSelectbox > div > div {
            background-color: #ffffff !important;
            border: 1px solid #1D3269 !important;
            border-radius: 6px !important;
            color: #1D3269 !important;
        }
        .stSelectbox div[role="listbox"] {
            background-color: #ffffff !important;
            border: 1px solid #ffffff !important;
        }
        .stSelectbox div[role="option"] {
            background-color: #ffffff !important;
            color: #1D3269 !important;
        }
        .stSelectbox div[role="option"]:hover {
            background-color: #1D3269 !important;
            color: #ffffff !important;
        
        }
        .stSlider [role="slider"] {
            background-color: #1D3269 !important;
            border: 2px solid #7FA536 !important;
        }

        /* Remove ticks e valores laterais */
        .stSlider div[data-testid="stTickBar"] {
            display: none !important;
        }
        
        /* Deixa o trilho preenchido do slider azul */
        .stSlider > div[data-baseweb="slider"] > div > div:nth-child(2) {
        }

        /* Botões */
        .stButton > button, .stDownloadButton > button {
            background: #7FA536 !important;
            color: #fff !important;
            border: none;
            border-radius: 6px;
            font-size: 15px;
            padding: 8px 20px;
            transition: all 0.2s ease;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            background: #94bf48 !important;
            transform: translateY(-2px);
        }

        audio {
            width: 100%;
            margin-top: 15px;
        }

        /* Centraliza os botões */
        .button-container {
            display: flex;
            gap: 12px;
            justify-content: center;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)


st.title("🎙️ Leitor de Texto do Informa")

# Entrada de texto
texto = st.text_area("Digite o texto para leitura:", "Olá, este é um teste com voz interativa.")

# Presets de vozes simuladas
voz_preset = st.selectbox("Escolha um preset de voz:", ["Padrão", "Masculino Grave", "Feminino Suave", "Criança Aguda"])

# Ajustes manuais
velocidade = st.slider("Velocidade", 0.5, 2.0, 1.0, 0.05)
pitch = st.slider("Pitch (Tom)", -20, 20, 0, 1)
volume = st.slider("Volume (dB)",-10, 10, 0, 1)

# Aplica preset escolhido
if voz_preset == "Masculino Grave":
    pitch = -4
    velocidade = 0.9
elif voz_preset == "Feminino Suave":
    pitch = 4
    velocidade = 1.1
elif voz_preset == "Criança Aguda":
    pitch = 8
    velocidade = 1.3

temp_audio = "temp_audio.mp3"
final_audio = "voz_final.mp3"

def gerar_audio(output_file):
    """Gera o áudio com ajustes usando gTTS e FFmpeg."""
    tts = gTTS(text=texto, lang="pt")
    tts.save(output_file)

    filters = []
    if pitch != 0:
        pitch_factor = 2 ** (pitch / 12.0)
        filters.append(f"asetrate=44100*{pitch_factor}")
        filters.append("aresample=44100")
    if velocidade != 1.0:
        filters.append(f"atempo={velocidade}")
    if volume != 0:
        filters.append(f"volume={volume}dB")

    filter_str = ",".join(filters) if filters else "anull"

    temp_processed = "processed.mp3"
    subprocess.run([
        FFMPEG_PATH, "-y",
        "-i", output_file,
        "-af", filter_str,
        temp_processed
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.replace(temp_processed, output_file)

# Botões
if st.button("🔊 Preview"):
    if texto.strip():
        gerar_audio(temp_audio)
        with open(temp_audio, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
            """,
            unsafe_allow_html=True
        )

if st.button("💾 Gerar e Baixar"):
    gerar_audio(final_audio)
    with open(final_audio, "rb") as f:
        st.download_button("Baixar MP3", data=f, file_name="voz_final.mp3", mime="audio/mp3")
