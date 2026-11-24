from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.schemas import RobustnessRunRequest, RobustnessResult
from backend.app.services.robustness_service import robustness_service

router = APIRouter(prefix="/robustness", tags=["Robustness"])

@router.post("/run", response_model=List[RobustnessResult])
def run_robustness_test(request: RobustnessRunRequest, db: Session = Depends(get_db)):
    try:
        results = robustness_service.evaluate_robustness(db, request)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
