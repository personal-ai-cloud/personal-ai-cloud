import gradio as gr
import requests

BACKEND_URL = "http://localhost:8000"

def chat(msg, history):
    r = requests.post(f"{BACKEND_URL}/chat", json={"message": msg}).json()
    return history + [(msg, r["reply"])]

gr.ChatInterface(chat, title="Personal AI").launch()
