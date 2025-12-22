from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class Msg(BaseModel):
    message: str

@app.post("/chat")
def chat(m: Msg):
    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "تو یک دستیار شخصی فارسی هستی"},
            {"role": "user", "content": m.message}
        ]
    )
    return {"reply": res.choices[0].message["content"]}
import json

MEMORY_FILE = "memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {"name": "", "preferences": {}}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)
