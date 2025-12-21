import os
import gradio as gr
import requests

def chat(message):
    if not message:
        return "پیامی وارد نکردی 🙂"
    return f"شما گفتید: {message}"

demo = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(label="پیام شما"),
    outputs=gr.Textbox(label="پاسخ"),
    title="هوش مصنوعی شخصی",
    description="نسخه تست روی Render"
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )
