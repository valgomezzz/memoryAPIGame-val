from fastapi import FastAPI
from api import router as memory_router

app = FastAPI(
    title="Memory Game API",
    description="API para gestionar el juego de memoria",
    version="1.0.0"
)

app.include_router(memory_router)

@app.get("/")
def home():
    return {"message": "🧠 Memory Game API funcionando correctamente"}