from fastapi import FastAPI

from app.api.v1.endpoints.payments import router
from app.sentry import init_sentry

app = FastAPI(
    title="Unified Payment Provider API",
)

init_sentry(app)

app.include_router(router)