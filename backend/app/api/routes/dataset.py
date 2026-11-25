from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import os
import shutil
import pandas as pd

from app.core.database import get_db
from app.core.models import Dataset, DatasetRecord
from app.core.schemas import DatasetResponse, DatasetStats, ColumnConfigUpdate
from app.services.dataset_service import DatasetService

router = APIRouter(prefix="/datasets", tags=["datasets"])
service = DatasetService()

@router.get("", response_model=List[DatasetResponse])
def get_datasets(db: Session = Depends(get_db)):
    return service.list_datasets(db)

@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    ds = service.get_dataset(db, dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return ds

@router.get("/{dataset_id}/preview")
def get_preview(dataset_id: int, limit: int = 15, db: Session = Depends(get_db)):
    preview = service.get_dataset_preview(db, dataset_id, limit=limit)
    if not preview:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return preview

@router.get("/{dataset_id}/stats", response_model=DatasetStats)
def get_stats(dataset_id: int, db: Session = Depends(get_db)):
    stats = service.get_dataset_stats(db, dataset_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return stats

@router.post("/upload", response_model=DatasetResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    modality: Optional[str] = None,
    task_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    upload_dir = "backend/datasets/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    dataset_name = name or file.filename.rsplit(".", 1)[0]
    return service.load_dataset_file(
        db=db,
        file_path=file_path,
        name=dataset_name,
        modality=modality,
        task_type=task_type
    )

@router.post("/{dataset_id}/config", response_model=DatasetResponse)
def update_column_config(
    dataset_id: int,
    config: ColumnConfigUpdate,
    db: Session = Depends(get_db)
):
    ds = service.update_column_config(db, dataset_id, config)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return ds

@router.post("/seed-benchmarks")
def seed_benchmarks(db: Session = Depends(get_db)):
    loaded = service.seed_default_benchmarks(db)
    return {"status": "success", "seeded_datasets": len(loaded)}
