from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.models import TrainingExperiment
from backend.app.core.schemas import TrainingRunRequest, ExperimentResponse
from backend.app.services.training_service import training_service

router = APIRouter(prefix="/training", tags=["Training"])

@router.post("/run", response_model=ExperimentResponse)
def run_training_experiment(request: TrainingRunRequest, db: Session = Depends(get_db)):
    try:
        exp = training_service.run_experiment(db, request)
        details = training_service.get_experiment_details(db, exp.id)
        return details
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/experiments", response_model=List[ExperimentResponse])
def get_experiments(dataset_id: str = None, db: Session = Depends(get_db)):
    q = db.query(TrainingExperiment)
    if dataset_id:
        q = q.filter(TrainingExperiment.dataset_id == dataset_id)
    experiments = q.order_by(TrainingExperiment.created_at.desc()).all()

    results = []
    for exp in experiments:
        details = training_service.get_experiment_details(db, exp.id)
        results.append(details)
    return results
