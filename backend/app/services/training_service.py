"""
Service layer connecting ZeroLeakageExperiment with Database and API.
"""
from typing import Dict, Any, List, Optional
import pandas as pd
from sqlalchemy.orm import Session

from app.core.models import Dataset, DatasetRecord, TrainingExperiment, ModelMetrics
from app.ml.experiment import ZeroLeakageExperiment

class TrainingService:
    def __init__(self):
        self.experiment_runner = ZeroLeakageExperiment()

    def run_training_experiment(
        self,
        db: Session,
        dataset_id: int,
        model_name: str,
        algorithm: str = "synonym_replacement",
        target_column: Optional[str] = None,
        input_column: Optional[str] = None,
        test_size: float = 0.2
    ) -> Dict[str, Any]:
        """Loads dataset from database and runs zero-leakage training experiment."""
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            raise ValueError(f"Dataset {dataset_id} not found")

        records = db.query(DatasetRecord).filter(DatasetRecord.dataset_id == dataset_id).all()
        if not records:
            raise ValueError("No records found in dataset to train.")

        df = pd.DataFrame([r.data_json for r in records])

        tgt = target_column or dataset.target_column
        inp = input_column or dataset.input_column
        id_col = dataset.id_column
        modality = dataset.modality or "text"
        task_type = dataset.task_type or "classification"

        if not tgt:
            raise ValueError("Target column is required for model training.")

        res = self.experiment_runner.run_experiment(
            df=df,
            modality=modality,
            task_type=task_type,
            model_name=model_name,
            target_column=tgt,
            input_column=inp,
            id_column=id_col,
            algorithm=algorithm,
            test_size=test_size
        )

        # Persist experiment record
        exp_record = TrainingExperiment(
            dataset_id=dataset_id,
            model_name=model_name,
            task_type=task_type,
            test_size=test_size,
            random_state=42,
            baseline_accuracy=res["baseline_metrics"].get("accuracy", res["baseline_metrics"].get("r2")),
            augmented_accuracy=res["augmented_metrics"].get("accuracy", res["augmented_metrics"].get("r2")),
            baseline_macro_f1=res["baseline_metrics"].get("macro_f1", res["baseline_metrics"].get("mae")),
            augmented_macro_f1=res["augmented_metrics"].get("macro_f1", res["augmented_metrics"].get("mae")),
            baseline_metrics_json=res["baseline_metrics"],
            augmented_metrics_json=res["augmented_metrics"]
        )
        db.add(exp_record)
        db.commit()
        db.refresh(exp_record)

        res["experiment_id"] = exp_record.id
        return res
