from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import assignments, cargo, events, routes, trucks, warehouses

app = FastAPI(
    title="MIDAS API",
    description="Multi-Agent Intelligent Logistics Coordination System",
    version="0.1.0",
)

# Allow the Vite dev server to call the API during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trucks.router)
app.include_router(cargo.router)
app.include_router(assignments.router)
app.include_router(warehouses.router)
app.include_router(routes.router)
app.include_router(events.router)


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
