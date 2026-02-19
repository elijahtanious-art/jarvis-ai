from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai

app = FastAPI()

# Load OpenAI key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

class Message(BaseModel):
    message: str

# Endpoint to check if API key is loaded
@app.get("/check_key")
async def check_key():
    if openai.api_key:
        return {"status": "API key loaded ✅"}
    else:
        return {"status": "API key NOT found ❌"}

# Chat endpoint using GPT-3.5
@app.post("/chat")
async def chat(msg: Message):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # <-- switched to GPT-3.5 for free tier
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
                {"role": "user", "content": msg.message}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
