from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import json
import os

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

def
