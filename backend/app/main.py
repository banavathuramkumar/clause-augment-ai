from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.database import Base, engine, SessionLocal
from backend.app.api.routes import (
    dataset,
    preprocessing,
    augmentation,
    validation,
    training,
    evaluation,
    robustness,
    export
)
from backend.app.services.dataset_service import dataset_service
from backend.app.utils.logger import logger

def init_db():
    logger.info("Initializing SQLite database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        sample = dataset_service.load_built_in_sample(db)
        logger.info(f"Loaded benchmark dataset '{sample.name}' (ID: {sample.id}).")
    except Exception as e:
        logger.error(f"Error seeding benchmark dataset: {e}")
    finally:
        db.close()

# Initialize tables and sample data upon module load
init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="ClauseAugment AI – Contract Clause Text Augmenter API",
    description="Controlled legal text data augmentation and ML classification pipeline for contract clauses.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(dataset.router, prefix="/api")
app.include_router(preprocessing.router, prefix="/api")
app.include_router(augmentation.router, prefix="/api")
app.include_router(validation.router, prefix="/api")
app.include_router(training.router, prefix="/api")
app.include_router(evaluation.router, prefix="/api")
app.include_router(robustness.router, prefix="/api")
app.include_router(export.router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ClauseAugment AI API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
