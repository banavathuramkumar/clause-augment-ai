from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import pandas as pd

from app.core.database import get_db
from app.core.models import Dataset, DatasetRecord, AugmentedRecord
from app.core.schemas import AugmentationGenerateRequest
from app.services.augmentation_service import AugmentationService
from app.services.dataset_service import DatasetService

router = APIRouter(prefix="/augmentation", tags=["augmentation"])
aug_service = AugmentationService()
ds_service = DatasetService()

@router.get("/algorithms")
def get_algorithms():
    return {
        "text": [
            {"id": "synonym_replacement", "name": "Synonym Replacement (WordNet)"},
            {"id": "sentence_restructuring", "name": "Sentence Restructuring"},
            {"id": "random_swap", "name": "Random Word Swap"},
            {"id": "random_insertion", "name": "Random Synonym Insertion"},
            {"id": "random_deletion", "name": "Random Deletion"},
            {"id": "gemini_context_aware", "name": "Google Gemini Context-Aware Paraphrasing", "available": aug_service.gemini_augmenter.is_available}
        ],
        "tabular": [
            {"id": "smote", "name": "SMOTE (Synthetic Minority Over-sampling)"},
            {"id": "random_oversample", "name": "Random Oversampling with Jitter"},
            {"id": "gaussian_noise", "name": "Gaussian Noise Injection"},
            {"id": "numerical_perturbation", "name": "Numerical Feature Perturbation (+/- 8%)"},
            {"id": "resample_categorical", "name": "Categorical Resampling"}
        ]
    }

@router.get("/gemini-status")
def gemini_status():
    return {
        "is_available": aug_service.gemini_augmenter.is_available,
        "model_name": aug_service.gemini_augmenter.model_name
    }

@router.get("/recommendations/{dataset_id}")
def get_recommendations(dataset_id: int, db: Session = Depends(get_db)):
    ds = ds_service.get_dataset(db, dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    stats = ds_service.get_dataset_stats(db, dataset_id)
    return aug_service.get_recommendations(stats.model_dump(), modality=ds.modality)

@router.post("/generate")
def generate_augmentation(req: AugmentationGenerateRequest, db: Session = Depends(get_db)):
    ds = ds_service.get_dataset(db, req.dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")

    records = db.query(DatasetRecord).filter(DatasetRecord.dataset_id == req.dataset_id).all()
    if not records:
        raise HTTPException(status_code=400, detail="No records found in dataset to augment")

    df = pd.DataFrame([r.data_json for r in records])

    result = aug_service.augment_dataframe(
        df=df,
        modality=ds.modality,
        input_column=ds.input_column,
        target_column=ds.target_column,
        id_column=ds.id_column,
        preserved_columns=ds.preserved_columns or [],
        algorithm=req.algorithm,
        num_variations=req.num_variations,
        validate=req.validate_augmented,
        **req.hyperparameters
    )

    # Persist augmented records to database
    for rec in result["augmented_records"]:
        aug_entry = AugmentedRecord(
            dataset_id=req.dataset_id,
            algorithm=req.algorithm,
            original_row_json=rec["original_data"],
            augmented_row_json=rec["augmented_data"],
            is_valid=rec["is_valid"],
            validation_score=rec["validation_score"],
            rejection_reason=rec["rejection_reason"]
        )
        db.add(aug_entry)
    db.commit()

    return result
