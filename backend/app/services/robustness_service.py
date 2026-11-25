import os
import re
import random
import joblib
from typing import Dict, Any, List
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sqlalchemy.orm import Session
from app.core.models import TrainingExperiment, Clause
from app.core.schemas import RobustnessResult, RobustnessRunRequest
from app.config import TRAINED_MODELS_DIR
from app.utils.logger import logger

class RobustnessEvaluationService:
    @staticmethod
    def apply_perturbation(text: str, p_type: str, seed: int = 42) -> str:
        rng = random.Random(seed)
        words = text.split()
        
        if p_type == "drafting_style_shift":
            # Shift standard legal phrasing to alternate contract style
            replacements = {
                "The Receiving Party shall": "Recipient agrees to",
                "disclose": "reveal or disseminate",
                "prior written consent": "advance written approval",
                "indemnify, defend, and hold harmless": "defend, indemnify and protect",
                "Either party may terminate": "This Agreement may be cancelled by either party",
                "without cause": "for convenience",
                "In no event shall": "Under no circumstances will",
                "applicable law": "governing statutory regulations",
                "promptly": "without undue delay",
                "sole discretion": "exclusive prerogative"
            }
            res = text
            for k, v in replacements.items():
                if k in res:
                    res = res.replace(k, v)
            return res

        elif p_type == "paraphrase_stress":
            # Replace non-critical descriptors with formal alternatives
            formal_subs = {
                "maintain": "preserve",
                "restrict": "limit",
                "promptly": "immediately",
                "request": "application",
                "reasonable": "commercially prudent",
                "deliverables": "work items",
                "dispute": "controversy",
                "arbitration": "arbitral proceedings",
                "arising out of": "stemming from"
            }
            res = text
            for k, v in formal_subs.items():
                pattern = re.compile(rf"\b{k}\b", re.IGNORECASE)
                res = pattern.sub(v, res)
            return res

        elif p_type == "punctuation_spacing":
            # Noise from scanned or pasted contract clauses
            res = text
            # Double spaces, spacing before commas or colons
            res = res.replace(", ", " , ").replace(". ", " . ")
            # Capitalize random non-initial word or lower first char
            return res

        elif p_type == "case_typo":
            # Real-world minor transcription variations
            res = text
            if len(words) > 5:
                # Lowercase a single capitalized mid-sentence word if not a Party
                words[2] = words[2].lower()
                res = " ".join(words)
            return res

        return text

    @staticmethod
    def evaluate_robustness(db: Session, request: RobustnessRunRequest) -> List[RobustnessResult]:
        exp = db.query(TrainingExperiment).filter(TrainingExperiment.id == request.experiment_id).first()
        if not exp:
            raise ValueError(f"Experiment {request.experiment_id} not found.")

        # Reconstruct held-out test set
        orig_clauses = db.query(Clause).filter(Clause.dataset_id == exp.dataset_id).all()
        orig_texts = [c.clause_text for c in orig_clauses]
        orig_labels = [c.clause_type for c in orig_clauses]

        _, X_test, _, y_test = train_test_split(
            orig_texts,
            orig_labels,
            train_size=exp.train_ratio,
            stratify=orig_labels,
            random_state=exp.random_state
        )

        # Load models
        path_a = TRAINED_MODELS_DIR / f"{exp.id}_orig.joblib"
        path_b = TRAINED_MODELS_DIR / f"{exp.id}_{exp.model_name}_{exp.feature_type}.joblib"

        if not path_a.exists() or not path_b.exists():
            raise FileNotFoundError("Model artifacts for this experiment could not be located on disk.")

        model_a = joblib.load(str(path_a))
        model_b = joblib.load(str(path_b))

        results = []
        for p_idx, p_type in enumerate(request.perturbation_types):
            perturbed_texts = [
                RobustnessEvaluationService.apply_perturbation(t, p_type, seed=exp.random_state + idx)
                for idx, t in enumerate(X_test)
            ]

            preds_a = model_a.predict(perturbed_texts)
            preds_b = model_b.predict(perturbed_texts)

            acc_a = round(float(accuracy_score(y_test, preds_a)), 4)
            acc_b = round(float(accuracy_score(y_test, preds_b)), 4)
            f1_a = round(float(f1_score(y_test, preds_a, average="macro", zero_division=0)), 4)
            f1_b = round(float(f1_score(y_test, preds_b, average="macro", zero_division=0)), 4)

            samples = []
            for orig, pert in zip(X_test[:2], perturbed_texts[:2]):
                samples.append({"original": orig, "perturbed": pert})

            acc_delta = round(acc_b - acc_a, 4)
            f1_delta = round(f1_b - f1_a, 4)

            results.append(RobustnessResult(
                perturbation_type=p_type,
                original_model_accuracy=acc_a,
                augmented_model_accuracy=acc_b,
                original_model_f1=f1_a,
                augmented_model_f1=f1_b,
                accuracy_delta=acc_delta,
                f1_delta=f1_delta,
                robustness_gain=round(f1_delta * 100.0, 2),
                sample_perturbations=samples
            ))

        return results

robustness_service = RobustnessEvaluationService()
