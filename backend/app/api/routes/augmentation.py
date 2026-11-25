from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.models import AugmentedClause
from backend.app.core.schemas import (
    AugmentationGenerateRequest,
    AugmentedClauseResponse,
    AugmentationApprovalRequest
)
from backend.app.services.augmentation_service import augmentation_service

router = APIRouter(prefix="/augmentation", tags=["Augmentation"])

@router.post("/generate", response_model=List[AugmentedClauseResponse])
def generate_augmentations(request: AugmentationGenerateRequest, db: Session = Depends(get_db)):
    try:
        created = augmentation_service.generate_augmentations(db, request)
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/results", response_model=List[AugmentedClauseResponse])
def get_augmentation_results(
    dataset_id: str,
    status: Optional[str] = None,
    technique: Optional[str] = None,
    limit: int = Query(default=100, le=500),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    q = db.query(AugmentedClause).filter(AugmentedClause.dataset_id == dataset_id)
    if status:
        q = q.filter(AugmentedClause.status == status)
    if technique:
        q = q.filter(AugmentedClause.technique == technique)
    results = q.order_by(AugmentedClause.created_at.desc()).offset(offset).limit(limit).all()
    return results

@router.post("/approve")
def approve_augmentations(request: AugmentationApprovalRequest, db: Session = Depends(get_db)):
    count = augmentation_service.update_approval_status(
        db, request.augmented_clause_ids, action="approve", reason=request.reason
    )
    return {"message": f"Successfully approved {count} clause variations.", "count": count}

@router.post("/reject")
def reject_augmentations(request: AugmentationApprovalRequest, db: Session = Depends(get_db)):
    count = augmentation_service.update_approval_status(
        db, request.augmented_clause_ids, action="reject", reason=request.reason
    )
    return {"message": f"Successfully rejected {count} clause variations.", "count": count}
