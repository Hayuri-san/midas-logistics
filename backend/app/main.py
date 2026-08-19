from fastapi import FastAPI

app = FastAPI(
    title="MIDAS API",
    description="Multi-Agent Intelligent Logistics Coordination System",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "project": "MIDAS",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }