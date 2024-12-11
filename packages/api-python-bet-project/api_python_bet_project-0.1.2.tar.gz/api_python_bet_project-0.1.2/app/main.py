from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from decouple import config

from routers import healthz, hello_world

app = FastAPI(
    title="api-python-bet-project",
    description=open("README.md", mode="r").read(),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(healthz.router)
app.include_router(hello_world.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(config("PORT", cast=int, default=5000)),
        log_level=str(config("LOG_LEVEL", cast=str, default="debug")),
        workers=int(config("WORKERS", cast=int, default=1)),
    )