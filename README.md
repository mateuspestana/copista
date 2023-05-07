# CopistaApp

## Descrição do Projeto
Projeto de exemplo que utiliza Streamlit, Whisper e Youtube para transcrever vozes em qualquer língua.

## Pré-requisitos
- Python 3.7+
- Whisper
- Streamlit
- PyTorch
- yt-dlp
- ffmpeg

## Sobre o Whisper
O Whisper é um modelo de deep learning que transcreve áudios em tempo real. O modelo foi treinado com 680.000 horas de áudio em idiomas diferentes.
O modelo é considerado um ASR, *automatic speech recognition*, ou seja, ele é capaz de transcrever áudios em tempo real em qualquer uma das línguas em que foi treinado.
A arquitetura do Whisper é a seguinte:
![Arquitetura do Whisper](https://openaicom.imgix.net/d9c13138-366f-49d3-b8bd-cb3f5a973a5b/asr-summary-of-model-architecture-desktop.svg?fm=auto&auto=compress,format&fit=min&w=1919&h=1551)  
O paper pode ser encontrado [aqui](https://cdn.openai.com/papers/whisper.pdf)!

## Sobre o autor
[Matheus C. Pestana](https://www.linkedin.com/in/matheus-pestana/)

Email: matheus.pestana@fgv.br

## TODO
- [ ] Adicionar suporte a criação de *voiceover* em inglês e português
- [ ] Adicionar suporte ao download do arquivo gravado ou do áudio do vídeo inserido