from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import pandas as pd

from app.core.database import get_db
from app.core.models import AugmentedRecord, Dataset
from app.services.validation_service import ValidationService

router = APIRouter(prefix="/validation", tags=["validation"])
val_service = ValidationService()

@router.get("/rules")
def get_validation_rules():
    return {
        "text_rules": [
            {"rule": "Cosine Similarity Threshold", "description": "Ensures augmented text semantic cosine similarity falls between [0.60, 0.98]."},
            {"rule": "Negation Consistency", "description": "Detects inversion of negation polarity ('not', 'never', 'no')."},
            {"rule": "Modal Obligation Check", "description": "Flags disappearance of imperative obligation modals ('shall', 'must', 'required')."},
            {"rule": "Numerical Entity Retention", "description": "Preserves critical metrics, quantities, currency values and dates."},
            {"rule": "Length Drift Boundary", "description": "Enforces output length within +/- 40% of original token count."}
        ],
        "tabular_rules": [
            {"rule": "Dynamic Physical Bounds", "description": "Enforces numerical values within 15% tolerance of observed distribution span."},
            {"rule": "Categorical Domain Validity", "description": "Rejects synthetic rows with unobserved or illegal category tokens."},
            {"rule": "Data Type Consistency", "description": "Guarantees integer/float preservation and null constraint adherence."}
        ]
    }

@router.get("/dataset/{dataset_id}")
def get_dataset_validation_records(
    dataset_id: int,
    status: str = Query("all", regex="^(all|passed|failed)$"),
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(AugmentedRecord).filter(AugmentedRecord.dataset_id == dataset_id)
    if status == "passed":
        query = query.filter(AugmentedRecord.is_valid == True)
    elif status == "failed":
        query = query.filter(AugmentedRecord.is_valid == False)

    records = query.order_by(AugmentedRecord.id.desc()).limit(limit).all()

    total_valid = db.query(AugmentedRecord).filter(AugmentedRecord.dataset_id == dataset_id, AugmentedRecord.is_valid == True).count()
    total_invalid = db.query(AugmentedRecord).filter(AugmentedRecord.dataset_id == dataset_id, AugmentedRecord.is_valid == False).count()

    return {
        "total_generated": total_valid + total_invalid,
        "valid_count": total_valid,
        "invalid_count": total_invalid,
        "pass_rate": round(total_valid / (total_valid + total_invalid), 4) if (total_valid + total_invalid) > 0 else 1.0,
        "records": [
            {
                "id": r.id,
                "algorithm": r.algorithm,
                "original_row": r.original_row_json,
                "augmented_row": r.augmented_row_json,
                "is_valid": r.is_valid,
                "validation_score": r.validation_score,
                "rejection_reason": r.rejection_reason
            }
            for r in records
        ]
    }
