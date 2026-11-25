import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.models import AugmentedClause, ValidationResult
from backend.app.core.schemas import ValidationRunRequest, ValidationItemResult
from backend.app.services.validation_service import validation_engine

router = APIRouter(prefix="/validation", tags=["Validation"])

@router.post("/run", response_model=List[ValidationItemResult])
def run_validation(request: ValidationRunRequest, db: Session = Depends(get_db)):
    augmented_clauses = db.query(AugmentedClause).filter(
        AugmentedClause.dataset_id == request.dataset_id
    ).all()

    if not augmented_clauses:
        raise HTTPException(status_code=404, detail="No augmented clauses found for this dataset.")

    results = []
    for aug in augmented_clauses:
        val_res = validation_engine.validate(
            orig_text=aug.original_text,
            aug_text=aug.augmented_text,
            threshold=request.similarity_threshold,
            enforce_negations=request.enforce_negations,
            enforce_modals=request.enforce_modal_verbs,
            enforce_keywords=request.enforce_keywords,
            enforce_numbers=request.enforce_numbers_dates
        )

        aug.similarity_score = val_res["similarity_score"]
        aug.status = val_res["status"]
        aug.validation_reason = val_res["reason"]

        val_rec = db.query(ValidationResult).filter(
            ValidationResult.augmented_clause_id == aug.id
        ).first()

        if not val_rec:
            val_rec = ValidationResult(
                augmented_clause_id=aug.id,
                similarity_score=val_res["similarity_score"],
                legal_keywords_preserved=val_res["legal_keywords_preserved"],
                negation_preserved=val_res["negation_preserved"],
                modal_verbs_preserved=val_res["modal_verbs_preserved"],
                numbers_dates_preserved=val_res["numbers_dates_preserved"],
                status=val_res["status"],
                flag_reasons=json.dumps(val_res["flag_reasons"])
            )
            db.add(val_rec)
        else:
            val_rec.similarity_score = val_res["similarity_score"]
            val_rec.legal_keywords_preserved = val_res["legal_keywords_preserved"]
            val_rec.negation_preserved = val_res["negation_preserved"]
            val_rec.modal_verbs_preserved = val_res["modal_verbs_preserved"]
            val_rec.numbers_dates_preserved = val_res["numbers_dates_preserved"]
            val_rec.status = val_res["status"]
            val_rec.flag_reasons = json.dumps(val_res["flag_reasons"])

        results.append(ValidationItemResult(
            id=val_rec.id or aug.id,
            augmented_clause_id=aug.id,
            original_text=aug.original_text,
            augmented_text=aug.augmented_text,
            technique=aug.technique,
            similarity_score=val_res["similarity_score"],
            legal_keywords_preserved=val_res["legal_keywords_preserved"],
            negation_preserved=val_res["negation_preserved"],
            modal_verbs_preserved=val_res["modal_verbs_preserved"],
            numbers_dates_preserved=val_res["numbers_dates_preserved"],
            status=val_res["status"],
            flag_reasons=val_res["flag_reasons"]
        ))

    db.commit()
    return results
