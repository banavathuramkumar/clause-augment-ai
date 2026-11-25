from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.schemas import ExperimentResponse
from backend.app.services.training_service import training_service

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])

@router.get("/{experiment_id}", response_model=ExperimentResponse)
def get_evaluation(experiment_id: str, db: Session = Depends(get_db)):
    try:
        return training_service.get_experiment_details(db, experiment_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
