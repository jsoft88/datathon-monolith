import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from factored_api.endpoints.chatbot import router as chatbot_router


def create_app() -> FastAPI:
    app = FastAPI(title="Factored API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(chatbot_router)
    return app


app = create_app()


def run() -> None:
    uvicorn.run("factored_api.main:app", host="0.0.0.0", port=8000, reload=True)
