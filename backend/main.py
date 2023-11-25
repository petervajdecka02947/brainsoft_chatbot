from fastapi import FastAPI
from routers.generation import router as chat_router
from routers.chat_history import router as chat_history_router

app = FastAPI(
    title="Generative AI Python SDK documentation",
    description="Braisoft API demo",
    version="1.0.0",
)


app.include_router(chat_router, tags=["generation"])
app.include_router(chat_history_router, tags=["mongo_db"])
