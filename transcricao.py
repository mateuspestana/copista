import streamlit as st
import whisper
from audiorecorder import audiorecorder
from yt_dlp import YoutubeDL
import time
import os
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=UserWarning)

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'outtmpl': 'audio.m4a',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
}

st.set_page_config(page_title="App de Transcrição", page_icon="🧊", layout="wide")

st.title('CopistaApp 🎤📝')
st.caption('Desenvolvido por Matheus C. Pestana - matheus.pestana@fgv.br')

@st.cache_resource
def load_model(tamanho):
    return whisper.load_model(tamanho)

def salva_audio(audio):
    with open("audio.wav", "wb") as f:
        f.write(audio.tobytes())

def salva_video(url):
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.download([url])

def transcreve(model, file):
    audio = whisper.load_audio(file)
    resultado = model.transcribe(audio)
    texto, lingua = resultado['text'], resultado['language']
    return texto, lingua


with st.sidebar:
    st.header('Configurações')
    tamanho = st.selectbox('Tamanho do modelo', ['tiny', 'base', 'small', 'medium', 'large'], index=2)
    with st.form(key='recording'):
        st.subheader('Gravação de voz')
        st.markdown('##### Aperte para gravar e parar')
        audio = audiorecorder("🎤Gravar", "⏹Parar de gravar")
        submit_rec = st.form_submit_button('Transcrever voz')

    with st.form(key='youtube'):
        st.subheader('Youtube')
        video = st.text_input('Insira o link do vídeo')
        submit_yt = st.form_submit_button('Transcrever vídeo')

placeholder = st.empty()
placeholder.markdown("""

### Grave um áudio ou cole a url de um vídeo do Youtube para transcrever.

Esse projeto foi desenvolvido com o intuito de experimentar a integração do streamlit com o Whisper, da OpenAI. 

O Whisper é um modelo de deep learning que transcreve áudios em tempo real. O modelo foi treinado com 680.000 horas de áudio em idiomas diferentes.

O modelo é considerado um ASR, *automatic speech recognition*, ou seja, ele é capaz de transcrever áudios em tempo real em qualquer uma das línguas em que foi treinado.

A arquitetura do Whisper é a seguinte:

![Arquitetura do Whisper](https://openaicom.imgix.net/d9c13138-366f-49d3-b8bd-cb3f5a973a5b/asr-summary-of-model-architecture-desktop.svg?fm=auto&auto=compress,format&fit=min&w=1919&h=1551)

O paper pode ser encontrado [aqui](https://cdn.openai.com/papers/whisper.pdf)
""")

if submit_rec:
    inicio = time.time()
    placeholder.subheader('Transcrição de áudio')
    with st.spinner('Baixando modelo...'):
        model = load_model(tamanho)
    if len(audio > 0):
        salva_audio(audio)
        try:
            with st.spinner('Transcrevendo...'):
                result = transcreve(model, 'audio.wav')
                os.remove('audio.wav')
                texto, lingua = result[0], result[1]
                st.markdown(f'#### Texto em {lingua}:')
                st.markdown(f'#### {texto}')
                st.caption(f'Tempo de transcrição: {time.time() - inicio:.2f} segundos')
                st.download_button('Baixar', texto, 'transcricao.txt')
        except Exception as e:
            st.error(f'Erro na transcrição. {e}')
    else:
        st.error('Nenhum áudio foi gravado.')

if submit_yt:
    if len(video) == 0:
        st.error('Insira uma url válida.')
    else:
        inicio = time.time()
        with st.spinner('Baixando modelo...'):
            model = load_model(tamanho)
        try:
            with st.spinner('Transcrevendo...'):
                salva_video(video)
                result = transcreve(model, 'audio.m4a')
                os.remove('audio.m4a')
                texto, lingua = result[0], result[1]
                st.markdown(f'#### Texto em {lingua}:')
                st.markdown(f'#### {texto}')
                st.caption(f'Tempo de transcrição: {time.time() - inicio:.2f} segundos')
                st.download_button('Baixar', texto, 'transcricao.txt')
        except Exception as e:
            st.error(f'Erro na transcrição. {e}')