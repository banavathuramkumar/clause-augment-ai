from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import pandas as pd
import json
import io

from app.core.database import get_db
from app.core.models import Dataset, DatasetRecord, AugmentedRecord, TrainingExperiment

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/dataset/{dataset_id}")
def export_dataset(
    dataset_id: int,
    format: str = Query("csv", regex="^(csv|json|jsonl)$"),
    include_augmented: bool = True,
    only_valid: bool = True,
    db: Session = Depends(get_db)
):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    orig_records = db.query(DatasetRecord).filter(DatasetRecord.dataset_id == dataset_id).all()
    rows = [r.data_json for r in orig_records]

    if include_augmented:
        aug_query = db.query(AugmentedRecord).filter(AugmentedRecord.dataset_id == dataset_id)
        if only_valid:
            aug_query = aug_query.filter(AugmentedRecord.is_valid == True)
        aug_records = aug_query.all()
        for r in aug_records:
            rows.append(r.augmented_row_json)

    df = pd.DataFrame(rows)

    if format == "csv":
        csv_data = df.to_csv(index=False)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={dataset.name}_augmented.csv"}
        )
    elif format == "jsonl":
        jsonl_data = "\n".join([json.dumps(row) for row in rows])
        return Response(
            content=jsonl_data,
            media_type="application/x-ndjson",
            headers={"Content-Disposition": f"attachment; filename={dataset.name}_augmented.jsonl"}
        )
    else: # json
        return JSONResponse(content=rows)

@router.get("/report/{dataset_id}")
def export_academic_report(dataset_id: int, db: Session = Depends(get_db)):
    """Exports structured academic evaluation summary."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    experiments = db.query(TrainingExperiment).filter(TrainingExperiment.dataset_id == dataset_id).order_by(TrainingExperiment.id.desc()).all()
    
    return {
        "title": f"ClauseAugment AI Academic Empirical Report: {dataset.name}",
        "modality": dataset.modality,
        "task_type": dataset.task_type,
        "total_experiments_conducted": len(experiments),
        "experiments": [
            {
                "id": exp.id,
                "model_name": exp.model_name,
                "task_type": exp.task_type,
                "baseline_accuracy": exp.baseline_accuracy,
                "augmented_accuracy": exp.augmented_accuracy,
                "accuracy_delta": round((exp.augmented_accuracy or 0) - (exp.baseline_accuracy or 0), 4),
                "baseline_f1": exp.baseline_macro_f1,
                "augmented_f1": exp.augmented_macro_f1,
                "f1_delta": round((exp.augmented_macro_f1 or 0) - (exp.baseline_macro_f1 or 0), 4),
                "baseline_metrics": exp.baseline_metrics_json,
                "augmented_metrics": exp.augmented_metrics_json
            }
            for exp in experiments
        ]
    }
