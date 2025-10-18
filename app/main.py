from fastapi import FastAPI, Request
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = FastAPI(title="DevSecOps Demo", version="1.0.0")

# Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"],
)

class PredictIn(BaseModel):
    text: str | None = None
    value: float | None = None

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = time.time() - start
    endpoint = request.url.path
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(elapsed)
    REQUEST_COUNT.labels(
        method=request.method, endpoint=endpoint, status_code=str(response.status_code)
    ).inc()
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict")
def predict(payload: PredictIn):
    # Dummy logic to demonstrate request handling
    if payload.value is not None:
        pred = 1 if payload.value >= 0 else 0
    else:
        text = (payload.text or "").lower()
        pred = 1 if any(k in text for k in ["good", "great", "excellent"]) else 0
    return {"prediction": pred}

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

# Ensure Response is imported last to avoid circular reference with metrics
from fastapi.responses import Response  # noqa: E402
