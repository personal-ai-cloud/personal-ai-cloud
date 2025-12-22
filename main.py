from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from openai import OpenAI
from gtts import gTTS
import os

# ----------------------------
# تنظیمات اولیه
# ----------------------------
app = FastAPI(title="Personal AI Cloud with TTS")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MEMORY_FILE = "memory.db"

# ----------------------------
# دیتابیس SQLite
# ----------------------------
DATABASE_URL = "sqlite:///./memory.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserMemory(Base):
    __tablename__ = "user_memory"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    name = Column(String, default="")
    favorite_color = Column(String, default="")
    last_question = Column(Text, default="")

Base.metadata.create_all(bind=engine)

# ----------------------------
# توابع کمکی
# ----------------------------
def get_memory(user_id: str):
    db = SessionLocal()
    memory = db.query(UserMemory).filter(UserMemory.user_id == user_id).first()
    if not memory:
        memory = UserMemory(user_id=user_id)
        db.add(memory)
        db.commit()
        db.refresh(memory)
    db.close()
    return memory

def save_memory(memory: UserMemory):
    db = SessionLocal()
    db.merge(memory)
    db.commit()
    db.close()

# ----------------------------
# تست سلامت سرور
# ----------------------------
@app.get("/")
def root():
    return {"status": "AI with TTS is running"}

# ----------------------------
# چت با حافظه چند کاره و TTS
# ----------------------------
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "default_user").strip()
    user_message = data.get("message", "").strip()

    if not user_message:
        raise HTTPException(status_code=422, detail="پیام کاربر خالی است")

    memory = get_memory(user_id)

    if memory.name == "":
        memory.name = user_message
        save_memory(memory)
        reply_text = f"خیلی خوشوقتم {memory.name} 😊 از این به بعد شما رو به خاطر می‌سپارم."
    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a helpful personal AI assistant. The user's name is {memory.name}."},
                {"role": "user", "content": user_message}
            ]
        )
        reply_text = response.choices[0].message.content
        memory.last_question = user_message
        save_memory(memory)

    # ساخت فایل صوتی TTS
    tts_file = f"tts_{user_id}.mp3"
    tts = gTTS(text=reply_text, lang="fa")
    tts.save(tts_file)

    return JSONResponse({
        "reply": reply_text,
        "tts_file": tts_file
    })

# ----------------------------
# دانلود فایل صوتی
# ----------------------------
@app.get("/tts/{user_id}")
def get_tts(user_id: str):
    tts_file = f"tts_{user_id}.mp3"
    if not os.path.exists(tts_file):
        raise HTTPException(status_code=404, detail="فایل صوتی یافت نشد")
    return FileResponse(tts_file, media_type="audio/mpeg", filename=tts_file)
