import json
import uuid
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.core.models import TrainingExperiment, ModelMetrics, Dataset, Clause, AugmentedClause
from backend.app.core.schemas import TrainingRunRequest, ExperimentResponse, MetricsDetail
from backend.app.ml.experiment import run_comparative_experiment
from backend.app.utils.logger import logger

class TrainingService:
    @staticmethod
    def run_experiment(db: Session, request: TrainingRunRequest) -> TrainingExperiment:
        dataset = db.query(Dataset).filter(Dataset.id == request.dataset_id).first()
        if not dataset:
            raise ValueError(f"Dataset {request.dataset_id} not found.")

        orig_clauses = db.query(Clause).filter(Clause.dataset_id == request.dataset_id).all()
        aug_query = db.query(AugmentedClause).filter(AugmentedClause.dataset_id == request.dataset_id)
        if request.use_approved_only:
            aug_query = aug_query.filter(AugmentedClause.status == "Accepted")
        aug_clauses = aug_query.all()

        orig_dicts = [
            {"id": c.id, "clause_id": c.clause_id, "clause_text": c.clause_text, "clause_type": c.clause_type}
            for c in orig_clauses
        ]
        aug_dicts = [
            {
                "id": a.id,
                "original_clause_id": a.original_clause_id,
                "augmented_text": a.augmented_text,
                "clause_type": a.clause_type,
                "status": a.status
            }
            for a in aug_clauses
        ]

        exp_id = str(uuid.uuid4())
        exp_name = f"{request.model_name} ({request.feature_type}) - Seed {request.random_state}"

        exp_results = run_comparative_experiment(
            original_clauses=orig_dicts,
            augmented_clauses=aug_dicts,
            model_name=request.model_name,
            feature_type=request.feature_type,
            train_ratio=request.train_ratio,
            random_state=request.random_state,
            experiment_id=exp_id
        )

        experiment = TrainingExperiment(
            id=exp_id,
            dataset_id=dataset.id,
            name=exp_name,
            model_name=request.model_name,
            feature_type=request.feature_type,
            train_ratio=request.train_ratio,
            random_state=request.random_state,
            original_train_size=exp_results["original_train_size"],
            augmented_train_size=exp_results["augmented_train_size"],
            test_size=exp_results["test_size"],
            model_artifact_path=exp_results["artifact_path"]
        )
        db.add(experiment)
        db.flush()

        # Save Metrics for Exp A (Original)
        ma = exp_results["metrics_a"]
        metric_a_rec = ModelMetrics(
            experiment_id=experiment.id,
            condition="Original",
            accuracy=ma["accuracy"],
            macro_precision=ma["macro_precision"],
            macro_recall=ma["macro_recall"],
            macro_f1=ma["macro_f1"],
            weighted_f1=ma["weighted_f1"],
            confusion_matrix_json=json.dumps(ma["confusion_matrix"]),
            classification_report_json=json.dumps(ma["classification_report"])
        )
        db.add(metric_a_rec)

        # Save Metrics for Exp B (Augmented)
        mb = exp_results["metrics_b"]
        metric_b_rec = ModelMetrics(
            experiment_id=experiment.id,
            condition="Augmented",
            accuracy=mb["accuracy"],
            macro_precision=mb["macro_precision"],
            macro_recall=mb["macro_recall"],
            macro_f1=mb["macro_f1"],
            weighted_f1=mb["weighted_f1"],
            confusion_matrix_json=json.dumps(mb["confusion_matrix"]),
            classification_report_json=json.dumps(mb["classification_report"])
        )
        db.add(metric_b_rec)

        db.commit()
        db.refresh(experiment)
        logger.info(f"Saved experiment {experiment.id}: Original Macro F1 = {ma['macro_f1']:.4f}, Augmented Macro F1 = {mb['macro_f1']:.4f}")
        return experiment

    @staticmethod
    def get_experiment_details(db: Session, experiment_id: str) -> Dict[str, Any]:
        exp = db.query(TrainingExperiment).filter(TrainingExperiment.id == experiment_id).first()
        if not exp:
            raise ValueError(f"Experiment {experiment_id} not found.")

        metrics_recs = db.query(ModelMetrics).filter(ModelMetrics.experiment_id == experiment_id).all()
        metrics_dict: Dict[str, Any] = {}
        for m in metrics_recs:
            clf_rep = json.loads(m.classification_report_json)
            labels = [k for k in clf_rep.keys() if k not in {"accuracy", "macro avg", "weighted avg"}]
            metrics_dict[m.condition] = {
                "condition": m.condition,
                "accuracy": m.accuracy,
                "macro_precision": m.macro_precision,
                "macro_recall": m.macro_recall,
                "macro_f1": m.macro_f1,
                "weighted_f1": m.weighted_f1,
                "confusion_matrix": json.loads(m.confusion_matrix_json),
                "labels": sorted(labels),
                "classification_report": clf_rep
            }

        orig_m = metrics_dict.get("Original", {})
        aug_m = metrics_dict.get("Augmented", {})
        f1_delta = round(aug_m.get("macro_f1", 0) - orig_m.get("macro_f1", 0), 4)
        acc_delta = round(aug_m.get("accuracy", 0) - orig_m.get("accuracy", 0), 4)
        rel_f1 = 0.0
        if orig_m.get("macro_f1", 0) > 0:
            rel_f1 = round((f1_delta / orig_m["macro_f1"]) * 100.0, 2)

        return {
            "id": exp.id,
            "dataset_id": exp.dataset_id,
            "name": exp.name,
            "model_name": exp.model_name,
            "feature_type": exp.feature_type,
            "train_ratio": exp.train_ratio,
            "random_state": exp.random_state,
            "original_train_size": exp.original_train_size,
            "augmented_train_size": exp.augmented_train_size,
            "test_size": exp.test_size,
            "created_at": exp.created_at,
            "metrics": metrics_dict,
            "comparison": {
                "accuracy_delta": acc_delta,
                "macro_f1_delta": f1_delta,
                "relative_f1_improvement_pct": rel_f1,
                "performance_improved": f1_delta > 0
            }
        }

training_service = TrainingService()
