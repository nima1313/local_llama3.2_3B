import os
import tempfile
import streamlit as st
from embedchain import App
import base64
from streamlit_chat import message


def embedchain_bot(db_path):
    return App.from_config(
        config={
            "llm": {"provider": "ollama", "config": {"model": "llama3.2:latest", "max_tokens":250, 
                     "temperature": 0.5, "stream": True, "base_url": "http://localhost:11434"}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "ollama", "config": {"model": "llama3.2:latest", "base_url": "http://localhost:11434"}},
        }
    )

def display_pdf(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="400" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

st.title("PersoBot")
st.caption("This is a personal chatbot that works without internet. it's based on llama3.2:latest")

db_path = tempfile.mktemp()
if 'app' not in st.session_state:
    st.session_state.app = embedchain_bot(db_path)
if 'messages' not in st.session_state:
    st.session_state.messages = []
