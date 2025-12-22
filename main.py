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

def load_memory():memory = load_memory()

# اگر اسم کاربر خالیه، بپرس و ذخیره کن
if memory["name"] == "":
    memory["name"] = prompt.message  # فرض می‌کنیم اولین پیام اسم است
    save_memory(memory)
    return {"reply": f"خیلی خوشوقتم، {memory['name']}! از این به بعد شما رو یادم می‌مونم."}

# پاسخ AI بر اساس حافظه
user_name = memory["name"]
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"You are a helpful AI assistant that knows the user's name is {user_name}."},
        {"role": "user", "content": prompt.message}
    ]
)
return {"reply": response.choices[0].message.content}
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {"name": "", "preferences": {}}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)
