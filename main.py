from datetime import datetime

import uvicorn
from fastapi import FastAPI, Response
from prometheus_client import Counter, CONTENT_TYPE_LATEST, generate_latest

app = FastAPI(title="python-public")

http_requests = Counter(
    "http_requests_total", "Total HTTP requests", ["path", "status"]
)


@app.get("/health")
def health():
    http_requests.labels(path="/health", status="200").inc()
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/ready")
def ready():
    http_requests.labels(path="/ready", status="200").inc()
    return {"status": "ready"}


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/")
def root():
    http_requests.labels(path="/", status="200").inc()
    return {"service": "python-public", "version": "1.0.0"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
