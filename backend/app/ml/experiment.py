"""
Zero-Data-Leakage Experiment Orchestrator:
1. Splits raw data into Train (80%) and Test (20%) held-out split BEFORE any augmentation.
2. Trains Baseline Model solely on original Train set.
3. Augments ONLY the Train set.
4. Trains Augmented Model on (Original Train + Augmented Train).
5. Evaluates BOTH Baseline and Augmented models on the EXACT SAME unseen original Test set.
6. Computes relative gains and statistical delta.
"""
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from app.ml.classifiers import get_classifier, get_regressor
from app.ml.feature_extraction import create_text_pipeline, create_tabular_pipeline
from app.ml.metrics import compute_classification_metrics, compute_regression_metrics
from app.services.augmentation_service import AugmentationService

class ZeroLeakageExperiment:
    def __init__(self):
        self.aug_service = AugmentationService()

    def run_experiment(
        self,
        df: pd.DataFrame,
        modality: str,
        task_type: str, # classification or regression
        model_name: str,
        target_column: str,
        input_column: Optional[str] = None,
        numerical_columns: Optional[List[str]] = None,
        categorical_columns: Optional[List[str]] = None,
        id_column: Optional[str] = None,
        algorithm: str = "synonym_replacement",
        test_size: float = 0.2,
        random_state: int = 42,
        **kwargs
    ) -> Dict[str, Any]:
        """Runs baseline vs augmented model training with strict train/test isolation."""
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset.")

        clean_df = df.dropna(subset=[target_column]).copy()
        
        # 1. Zero data leakage train/test split
        is_classification = (task_type == "classification")
        stratify = clean_df[target_column] if (is_classification and clean_df[target_column].value_counts().min() > 1) else None

        train_df, test_df = train_test_split(
            clean_df,
            test_size=test_size,
            random_state=random_state,
            stratify=stratify
        )

        # 2. Setup Transformers & Preprocessing
        if modality == "text":
            if not input_column or input_column not in clean_df.columns:
                raise ValueError(f"Input text column '{input_column}' required.")
            preprocessor = create_text_pipeline()
            X_train_raw = train_df[input_column].astype(str)
            X_test_raw = test_df[input_column].astype(str)
            y_train = train_df[target_column].values
            y_test = test_df[target_column].values

            # Fit vectorizer ON TRAIN ONLY
            X_train_base = preprocessor.fit_transform(X_train_raw)
            X_test = preprocessor.transform(X_test_raw)
        else:
            # Tabular
            num_cols = numerical_columns or train_df.select_dtypes(include=[np.number]).columns.tolist()
            if target_column in num_cols:
                num_cols.remove(target_column)
            if id_column in num_cols:
                num_cols.remove(id_column)

            cat_cols = categorical_columns or train_df.select_dtypes(include=["object", "category"]).columns.tolist()
            if target_column in cat_cols:
                cat_cols.remove(target_column)
            if id_column in cat_cols:
                cat_cols.remove(id_column)

            preprocessor = create_tabular_pipeline(num_cols, cat_cols)
            # Fit transformer ON TRAIN ONLY
            X_train_base = preprocessor.fit_transform(train_df[num_cols + cat_cols])
            X_test = preprocessor.transform(test_df[num_cols + cat_cols])
            y_train = train_df[target_column].values
            y_test = test_df[target_column].values

        # 3. Fit Baseline Model
        if is_classification:
            base_model = get_classifier(model_name, random_state=random_state)
            base_model.fit(X_train_base, y_train)
            base_preds = base_model.predict(X_test)
            base_metrics = compute_classification_metrics(y_test, base_preds)
        else:
            base_model = get_regressor(model_name, random_state=random_state)
            base_model.fit(X_train_base, y_train)
            base_preds = base_model.predict(X_test)
            base_metrics = compute_regression_metrics(y_test, base_preds)

        # 4. Augment ONLY Training Split
        aug_result = self.aug_service.augment_dataframe(
            df=train_df,
            modality=modality,
            input_column=input_column,
            target_column=target_column,
            id_column=id_column,
            algorithm=algorithm,
            num_variations=1,
            validate=True,
            is_classification=is_classification,
            **kwargs
        )
        aug_records = [r["augmented_data"] for r in aug_result["augmented_records"] if r["is_valid"]]
        if aug_records:
            aug_train_df = pd.DataFrame(aug_records)
            combined_train_df = pd.concat([train_df, aug_train_df], ignore_index=True)
        else:
            combined_train_df = train_df.copy()

        # 5. Transform Combined Train Data (re-transform using the EXACT same preprocessor fitted on train)
        if modality == "text":
            X_train_aug = preprocessor.transform(combined_train_df[input_column].astype(str))
            y_train_aug = combined_train_df[target_column].values
        else:
            X_train_aug = preprocessor.transform(combined_train_df[num_cols + cat_cols])
            y_train_aug = combined_train_df[target_column].values

        # 6. Fit Augmented Model
        if is_classification:
            aug_model = get_classifier(model_name, random_state=random_state)
            aug_model.fit(X_train_aug, y_train_aug)
            aug_preds = aug_model.predict(X_test)
            aug_metrics = compute_classification_metrics(y_test, aug_preds)
            
            # Delta
            acc_delta = aug_metrics["accuracy"] - base_metrics["accuracy"]
            f1_delta = aug_metrics["macro_f1"] - base_metrics["macro_f1"]
            gain_summary = {
                "accuracy_delta": round(acc_delta, 4),
                "macro_f1_delta": round(f1_delta, 4),
                "improved": f1_delta >= 0 or acc_delta >= 0
            }
        else:
            aug_model = get_regressor(model_name, random_state=random_state)
            aug_model.fit(X_train_aug, y_train_aug)
            aug_preds = aug_model.predict(X_test)
            aug_metrics = compute_regression_metrics(y_test, aug_preds)

            r2_delta = aug_metrics["r2"] - base_metrics["r2"]
            mae_delta = base_metrics["mae"] - aug_metrics["mae"] # positive means reduced error
            gain_summary = {
                "r2_delta": round(r2_delta, 4),
                "mae_reduction": round(mae_delta, 4),
                "improved": r2_delta >= 0 or mae_delta >= 0
            }

        return {
            "model_name": model_name,
            "modality": modality,
            "task_type": task_type,
            "algorithm": algorithm,
            "train_size_original": len(train_df),
            "train_size_augmented": len(combined_train_df),
            "test_size": len(test_df),
            "baseline_metrics": base_metrics,
            "augmented_metrics": aug_metrics,
            "gain_summary": gain_summary,
            "zero_leakage_guaranteed": True
        }
