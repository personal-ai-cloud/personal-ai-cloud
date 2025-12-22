from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
import json

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MEMORY_FILE = "memory.json"

class Prompt(BaseModel):
    message: str


def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {"name": ""}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)


@app.post("/chat")
def chat(prompt: Prompt):
    memory = load_memory()

    # اگر اسم هنوز ذخیره نشده
    if memory["name"] == "":
        memory["name"] = prompt.message.strip()
        save_memory(memory)
        return {
            "reply": f"خیلی خوشوقتم {memory['name']}! از این به بعد یادت می‌مونم 😊"
        }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a friendly Persian AI assistant. The user's name is {memory['name']}."
            },
            {
                "role": "user",
                "content": prompt.message
            }
        ]
    )

    return {"reply": response.choices[0].message.content}
