from datetime import datetime, timezone
import os
import random
import uuid

from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI(title="Deployment Lab - GREEN")


def fail_rate() -> float:
    raw_value = os.getenv("FAIL_RATE", "0.0")
    try:
        value = float(raw_value)
    except ValueError:
        value = 0.0
    return max(0.0, min(1.0, value))


def response_payload(message: str) -> dict:
    return {
        "version": "green",
        "hostname": os.getenv("HOSTNAME", "unknown"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": str(uuid.uuid4())[:8],
        "random_value": random.randint(1000, 9999),
        "message": message,
        "fail_rate": fail_rate(),
    }


@app.get("/")
def home():
    if random.random() < fail_rate():
        return JSONResponse(
            status_code=500,
            content=response_payload("New release failed this request"),
        )

    return response_payload("New release candidate")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": "green", "fail_rate": fail_rate()}
