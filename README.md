# Unified Payment Gateway

A FastAPI-based payment gateway service for creating payments, retrieving payment details, and processing provider webhooks.

## Features

- Async FastAPI application
- PostgreSQL backend with SQLAlchemy async ORM
- Webhook processing to update payment status
- Sentry integration for distributed error tracking
- Configurable via environment variables
- Structured logging support

## Prerequisites

- Python 3.11+ (project dependencies use modern async SQLAlchemy and FastAPI)
- PostgreSQL database
- `python-venv` for local virtual environments

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the example environment file:

```bash
cp .env.example .env
```

4. Edit `.env` and configure your database and webhook secret:

```dotenv
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
WEBHOOK_SECRET=super-secret-webhook-token
ENV=development
DEBUG=False
```

5. Start the application:

```bash
uvicorn app.main:app --reload
```

## Configuration

The application reads settings from `.env` using `pydantic-settings` and `python-dotenv`.

Required values:

- `DATABASE_URL` — Async SQLAlchemy connection string for PostgreSQL
- `WEBHOOK_SECRET` — Secret token required by webhook requests

Optional Sentry values:

- `SENTRY_DSN`
- `SENTRY_ENVIRONMENT`
- `SENTRY_RELEASE`
- `SENTRY_TRACES_SAMPLE_RATE`
- `SENTRY_PROFILES_SAMPLE_RATE`

## API Endpoints

### Create Payment

`POST /payments`

Headers:

- `Idempotency-Key`: unique key for request idempotency

Body:

```json
{
  "amount": 100.0,
  "currency": "USD",
  "customer_id": "customer_123",
  "provider": "stripe"
}
```

Response:

```json
{
  "id": 1,
  "provider_reference": "ref_abc123",
  "amount": 100.0,
  "currency": "USD",
  "status": "processing"
}
```

### Get Payment

`GET /payments/{payment_id}`

Response:

```json
{
  "id": 1,
  "provider_reference": "ref_abc123",
  "amount": 100.0,
  "currency": "USD",
  "status": "processing"
}
```

### Webhook Processing

`POST /webhooks/{provider}`

Headers:

- `X-Webhook-Secret`: webhook shared secret

Body:

Provider-specific payloads are normalized by each provider implementation.

Response:

```json
{
  "message": "Webhook processed successfully",
  "payment_id": 1,
  "status": "completed"
}
```

## Logging and Error Tracking

- Application logging is initialized in `app.logging`
- Webhook requests and payment operations emit structured log entries
- Sentry is configured via environment variables and initialized in `app.sentry`

## Notes

- This repository does not include database migration tooling. Create tables using SQLAlchemy models or add Alembic support if needed.
- Use `DEBUG=True` only in local development.

## License

This project does not include a license file. Add one if you plan to publish or share the code.
