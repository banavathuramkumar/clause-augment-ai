import sys
from pathlib import Path

# Ensure backend directory is in sys.path regardless of where uvicorn is invoked from
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import PROJECT_NAME, API_V1_STR
from app.core.database import init_db, SessionLocal
from app.services.dataset_service import DatasetService
from app.api.routes import (
    dataset,
    augmentation,
    validation,
    training,
    export
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables and load pre-seeded benchmarks synchronously
    init_db()
    try:
        db = SessionLocal()
        DatasetService().seed_default_benchmarks(db)
        db.close()
    except Exception as e:
        print(f"Benchmark seeding status: {e}")
    yield

app = FastAPI(
    title=PROJECT_NAME,
    description="Universal Data Augmentation & ML Robustness Platform for Text and Tabular Data",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dataset.router, prefix=API_V1_STR)
app.include_router(augmentation.router, prefix=API_V1_STR)
app.include_router(validation.router, prefix=API_V1_STR)
app.include_router(training.router, prefix=API_V1_STR)
app.include_router(export.router, prefix=API_V1_STR)

@app.get("/")
def root():
    return {
        "status": "online",
        "app": PROJECT_NAME,
        "version": "2.0.0",
        "supported_modalities": ["text", "tabular"],
        "supported_tasks": ["classification", "regression", "unlabeled"]
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
