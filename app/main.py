from fastapi import FastAPI

from app.api.v1.endpoints.payments import router as payments_router
from app.api.v1.endpoints.webhooks import router as webhooks_router
from app.sentry import init_sentry

app = FastAPI(
    title="Unified Payment Provider API",
)

init_sentry(app)

app.include_router(payments_router)
app.include_router(webhooks_router)