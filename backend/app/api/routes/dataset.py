import io
import csv
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.models import Dataset, Clause
from backend.app.core.schemas import DatasetResponse, ClauseResponse, DatasetStats, DatasetExpansionSummary
from backend.app.services.dataset_service import dataset_service

router = APIRouter(prefix="/datasets", tags=["Datasets"])

@router.get("", response_model=List[DatasetResponse])
def get_datasets(db: Session = Depends(get_db)):
    datasets = db.query(Dataset).order_by(Dataset.created_at.desc()).all()
    # If empty, automatically load built-in sample
    if not datasets:
        sample = dataset_service.load_built_in_sample(db)
        datasets = [sample]

    results = []
    for d in datasets:
        clauses = db.query(Clause).filter(Clause.dataset_id == d.id).all()
        stats = dataset_service.get_stats(clauses)
        results.append(DatasetResponse(
            id=d.id,
            name=d.name,
            description=d.description,
            filename=d.filename,
            total_clauses=d.total_clauses,
            num_categories=d.num_categories,
            created_at=d.created_at,
            stats=stats
        ))
    return results

@router.post("/upload", response_model=DatasetResponse)
async def upload_dataset(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    filename = file.filename or "uploaded_dataset"
    records = []

    try:
        if filename.endswith(".csv"):
            text = contents.decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            for row in reader:
                records.append(row)
        elif filename.endswith(".json"):
            records = json.loads(contents.decode("utf-8"))
            if isinstance(records, dict) and "clauses" in records:
                records = records["clauses"]
        else:
            raise HTTPException(status_code=400, detail="Only CSV and JSON dataset formats are supported.")

        dataset = dataset_service.create_dataset_from_records(
            db=db,
            name=name,
            records=records,
            description=description,
            filename=filename
        )
        clauses = db.query(Clause).filter(Clause.dataset_id == dataset.id).all()
        stats = dataset_service.get_stats(clauses)

        return DatasetResponse(
            id=dataset.id,
            name=dataset.name,
            description=dataset.description,
            filename=dataset.filename,
            total_clauses=dataset.total_clauses,
            num_categories=dataset.num_categories,
            created_at=dataset.created_at,
            stats=stats
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process dataset: {str(e)}")

@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(dataset_id: str, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    clauses = db.query(Clause).filter(Clause.dataset_id == dataset.id).all()
    stats = dataset_service.get_stats(clauses)
    return DatasetResponse(
        id=dataset.id,
        name=dataset.name,
        description=dataset.description,
        filename=dataset.filename,
        total_clauses=dataset.total_clauses,
        num_categories=dataset.num_categories,
        created_at=dataset.created_at,
        stats=stats
    )

@router.get("/{dataset_id}/clauses", response_model=List[ClauseResponse])
def get_clauses(
    dataset_id: str,
    category: Optional[str] = None,
    limit: int = Query(default=100, le=500),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    q = db.query(Clause).filter(Clause.dataset_id == dataset_id)
    if category:
        q = q.filter(Clause.clause_type == category)
    clauses = q.offset(offset).limit(limit).all()
    return clauses

@router.get("/{dataset_id}/expansion", response_model=DatasetExpansionSummary)
def get_expansion(dataset_id: str, db: Session = Depends(get_db)):
    try:
        return dataset_service.get_expansion_summary(db, dataset_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
