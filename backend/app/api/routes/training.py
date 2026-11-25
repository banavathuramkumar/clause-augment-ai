from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.core.database import get_db
from app.core.schemas import TrainingRequest, ExperimentResponse
from app.services.training_service import TrainingService

router = APIRouter(prefix="/training", tags=["training"])
service = TrainingService()

@router.get("/models")
def get_supported_models():
    return {
        "classification": [
            {"id": "logistic_regression", "name": "Logistic Regression (TF-IDF / Scaled)"},
            {"id": "linear_svc", "name": "Linear Support Vector Classifier (LinearSVC)"},
            {"id": "multinomial_nb", "name": "Multinomial Naive Bayes"},
            {"id": "random_forest", "name": "Random Forest Classifier"},
            {"id": "decision_tree", "name": "Decision Tree Classifier"}
        ],
        "regression": [
            {"id": "linear_regression", "name": "Ordinary Least Squares Linear Regression"},
            {"id": "ridge", "name": "Ridge Regression (L2 Regularized)"},
            {"id": "random_forest_regressor", "name": "Random Forest Regressor"}
        ]
    }

@router.post("/run", response_model=ExperimentResponse)
def run_experiment(req: TrainingRequest, db: Session = Depends(get_db)):
    try:
        return service.run_training_experiment(
            db=db,
            dataset_id=req.dataset_id,
            model_name=req.model_name,
            algorithm=req.algorithm,
            test_size=req.test_size
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
