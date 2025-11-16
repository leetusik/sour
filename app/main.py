from fastapi import FastAPI

from app.config import settings

app = FastAPI(title="Sour")

@app.get("/health")
async def health():
    return {"status": "ok"}