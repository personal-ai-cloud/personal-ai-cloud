from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import json
from openai import OpenAI

# ----------------------------
# تنظیمات اولیه
# ----------------------------
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MEMORY_FILE = "memory.json"

# ----------------------------
# توابع حافظه
# ----------------------------
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"name": ""}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# ----------------------------
# تست سلامت سرور
# ----------------------------
@app.get("/")
def root():
    return {"status": "AI is running"}

# ----------------------------
# چت با حافظه شخصی
# ----------------------------
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "").strip()

    memory = load_memory()

    # اگر اسم ذخیره نشده
    if memory["name"] == "":
        memory["name"] = user_message
        save_memory(memory)
        return JSONResponse({
            "reply": f"خیلی خوشوقتم {memory['name']} 😊 از این به بعد شما رو به خاطر می‌سپارم."
        })

    user_name = memory["name"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful personal AI assistant. The user's name is {user_name}."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return JSONResponse({
        "reply": response.choices[0].message.content
    })
