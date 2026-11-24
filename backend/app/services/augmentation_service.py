import json
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.core.models import Clause, AugmentedClause, ValidationResult, Dataset
from backend.app.core.schemas import AugmentationGenerateRequest
from backend.app.algorithms.synonym_replacement import SynonymReplacementAugmenter
from backend.app.algorithms.random_insertion import RandomInsertionAugmenter
from backend.app.algorithms.random_swap import RandomSwapAugmenter
from backend.app.algorithms.random_deletion import RandomDeletionAugmenter
from backend.app.algorithms.sentence_restructuring import SentenceRestructuringAugmenter
from backend.app.algorithms.back_translation import BackTranslationAugmenter
from backend.app.services.validation_service import validation_engine
from backend.app.utils.logger import logger

class AugmentationService:
    def __init__(self):
        self.algorithms = {
            "synonym_replacement": SynonymReplacementAugmenter(),
            "random_insertion": RandomInsertionAugmenter(),
            "random_swap": RandomSwapAugmenter(),
            "random_deletion": RandomDeletionAugmenter(),
            "sentence_restructuring": SentenceRestructuringAugmenter(),
            "back_translation": BackTranslationAugmenter(),
        }

    def generate_augmentations(self, db: Session, request: AugmentationGenerateRequest) -> List[AugmentedClause]:
        dataset = db.query(Dataset).filter(Dataset.id == request.dataset_id).first()
        if not dataset:
            raise ValueError(f"Dataset with ID {request.dataset_id} not found.")

        query = db.query(Clause).filter(Clause.dataset_id == request.dataset_id)
        if request.selected_categories:
            query = query.filter(Clause.clause_type.in_(request.selected_categories))
        clauses = query.all()

        created_augmented = []
        seed = request.random_seed

        for clause in clauses:
            for tech_name in request.techniques:
                augmenter = self.algorithms.get(tech_name)
                if not augmenter:
                    continue

                if tech_name == "back_translation" and not getattr(augmenter, "is_available", False):
                    continue

                variations = augmenter.generate(clause.clause_text, n=request.multiplier, seed=seed)
                seed += 1

                for var_text in variations:
                    # Clean trailing/leading spaces
                    clean_var = var_text.strip()
                    
                    val_res = validation_engine.validate(
                        orig_text=clause.clause_text,
                        aug_text=clean_var,
                        threshold=request.similarity_threshold
                    )

                    aug_record = AugmentedClause(
                        dataset_id=dataset.id,
                        original_clause_id=clause.id,
                        technique=tech_name,
                        original_text=clause.clause_text,
                        augmented_text=clean_var,
                        clause_type=clause.clause_type,
                        random_seed=seed,
                        status=val_res["status"],
                        validation_reason=val_res["reason"],
                        similarity_score=val_res["similarity_score"]
                    )
                    db.add(aug_record)
                    db.flush()

                    val_record = ValidationResult(
                        augmented_clause_id=aug_record.id,
                        similarity_score=val_res["similarity_score"],
                        legal_keywords_preserved=val_res["legal_keywords_preserved"],
                        negation_preserved=val_res["negation_preserved"],
                        modal_verbs_preserved=val_res["modal_verbs_preserved"],
                        numbers_dates_preserved=val_res["numbers_dates_preserved"],
                        status=val_res["status"],
                        flag_reasons=json.dumps(val_res["flag_reasons"])
                    )
                    db.add(val_record)
                    created_augmented.append(aug_record)

        db.commit()
        logger.info(f"Generated {len(created_augmented)} augmented clauses for dataset {request.dataset_id}.")
        return created_augmented

    def update_approval_status(
        self, db: Session, clause_ids: List[str], action: str, reason: Optional[str] = None
    ) -> int:
        status_value = "Accepted" if action == "approve" else "Rejected"
        records = db.query(AugmentedClause).filter(AugmentedClause.id.in_(clause_ids)).all()
        for r in records:
            r.status = status_value
            if reason:
                r.validation_reason = reason
            if r.validation_result:
                r.validation_result.status = status_value
        db.commit()
        return len(records)

augmentation_service = AugmentationService()
