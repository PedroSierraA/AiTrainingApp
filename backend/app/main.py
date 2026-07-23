from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import agents, user_config

app = FastAPI(title="Training App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router, prefix="/api/v1")
app.include_router(user_config.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok", "env": "local"}
