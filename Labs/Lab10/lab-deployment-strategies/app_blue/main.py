from datetime import datetime, timezone
import os
import random
import uuid

from fastapi import FastAPI


app = FastAPI(title="Deployment Lab - BLUE")


def response_payload() -> dict:
    return {
        "version": "blue",
        "hostname": os.getenv("HOSTNAME", "unknown"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": str(uuid.uuid4())[:8],
        "random_value": random.randint(1000, 9999),
        "message": "Stable production version",
    }


@app.get("/")
def home() -> dict:
    return response_payload()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": "blue"}
