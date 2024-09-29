import os
import tempfile
import streamlit as st
from embedchain import App
import base64
from streamlit_chat import message


def embedchain_bot(db_path):
    return App.from_config(
        config={
            "llm": {"provider": "ollama", "config": {"model": "llama3.2:latest", "max_tokens":300, 
                     "temprature": 0.5, "stram": True, "base_url": "http://localhost:11434"}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "ollama", "config": {"model": "llama3.2:lastest", "base_url": "http://localhost:11434"}},
        }
    )