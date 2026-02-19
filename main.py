from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Message(BaseModel):
    message: str

@app.get("/check_key")
async def check_key():
    if openai.api_key:
        return {"status": "API key loaded ✅"}
    else:
        return {"status": "API key NOT found ❌"}

@app.post("/chat")
async def chat(msg: Message):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Jarvis, a smart AI assistant."},
            {"role": "user", "content": msg.message}
        ]
    )

    return {"response": response.choices[0].message["content"]}
