from fastapi import FastAPI

from app.api.v1.endpoints.payments import router

app = FastAPI(
    title="Unified Payment Provider API",
)

app.include_router(router)