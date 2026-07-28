from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.api.chat import router as chat_router


app = FastAPI(title = "Companion AI")
app.include_router(chat_router, prefix = "/api")

@app.get("/")

def health_check() :
    return {"status": "Companion AI is running"}