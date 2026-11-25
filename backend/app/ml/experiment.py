import os
import joblib
from typing import Dict, Any, List, Tuple
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from backend.app.ml.feature_extraction import get_vectorizer
from backend.app.ml.classifiers import get_classifier
from backend.app.ml.metrics import compute_all_metrics
from backend.app.config import TRAINED_MODELS_DIR
from backend.app.utils.logger import logger

def run_comparative_experiment(
    original_clauses: List[Dict[str, Any]],  # list of dicts with id, clause_id, clause_text, clause_type
    augmented_clauses: List[Dict[str, Any]], # list of dicts with original_clause_id, augmented_text, clause_type, status
    model_name: str = "LogisticRegression",
    feature_type: str = "tfidf_unigram",
    train_ratio: float = 0.8,
    random_state: int = 42,
    experiment_id: str = "exp_default"
) -> Dict[str, Any]:
    """
    Executes a leakage-free comparative evaluation between:
    - Experiment A: Model trained solely on original training partition.
    - Experiment B: Model trained on original training partition + augmented training partition.
    Both are evaluated against the IDENTICAL held-out original test partition.
    """
    if len(original_clauses) < 10:
        raise ValueError("Dataset is too small to perform stratified train/test split.")

    # 1. Stratified split of original clauses
    orig_ids = [c["id"] for c in original_clauses]
    orig_texts = [c["clause_text"] for c in original_clauses]
    orig_labels = [c["clause_type"] for c in original_clauses]

    # Unique labels
    unique_labels = sorted(list(set(orig_labels)))

    train_ids, test_ids, X_train_orig, X_test, y_train_orig, y_test = train_test_split(
        orig_ids,
        orig_texts,
        orig_labels,
        train_size=train_ratio,
        stratify=orig_labels,
        random_state=random_state
    )

    train_id_set = set(train_ids)

    # 2. Filter augmented clauses: STRICTLY only augmentations belonging to train_ids!
    aug_train_texts = []
    aug_train_labels = []
    for aug in augmented_clauses:
        if aug["original_clause_id"] in train_id_set and aug.get("status") in {"Accepted", "Pending"}:
            aug_train_texts.append(aug["augmented_text"])
            aug_train_labels.append(aug["clause_type"])

    X_train_augmented = list(X_train_orig) + aug_train_texts
    y_train_augmented = list(y_train_orig) + aug_train_labels

    logger.info(
        f"Experiment Split: {len(X_train_orig)} original train, "
        f"{len(aug_train_texts)} augmented train ({len(X_train_augmented)} total), "
        f"{len(X_test)} test."
    )

    # 3. Train Experiment A (Original Only)
    vec_a = get_vectorizer(feature_type)
    clf_a = get_classifier(model_name, random_state=random_state)
    pipeline_a = Pipeline([("tfidf", vec_a), ("clf", clf_a)])
    pipeline_a.fit(X_train_orig, y_train_orig)
    preds_a = pipeline_a.predict(X_test)
    metrics_a = compute_all_metrics(y_test, preds_a, labels=unique_labels)
    metrics_a["condition"] = "Experiment A: Original Dataset"

    # 4. Train Experiment B (Augmented)
    vec_b = get_vectorizer(feature_type)
    clf_b = get_classifier(model_name, random_state=random_state)
    pipeline_b = Pipeline([("tfidf", vec_b), ("clf", clf_b)])
    pipeline_b.fit(X_train_augmented, y_train_augmented)
    preds_b = pipeline_b.predict(X_test)
    metrics_b = compute_all_metrics(y_test, preds_b, labels=unique_labels)
    metrics_b["condition"] = "Experiment B: Augmented Dataset"

    # 5. Compute comparative deltas
    acc_delta = round(metrics_b["accuracy"] - metrics_a["accuracy"], 4)
    f1_delta = round(metrics_b["macro_f1"] - metrics_a["macro_f1"], 4)
    weighted_f1_delta = round(metrics_b["weighted_f1"] - metrics_a["weighted_f1"], 4)

    rel_improvement = 0.0
    if metrics_a["macro_f1"] > 0:
        rel_improvement = round(((metrics_b["macro_f1"] - metrics_a["macro_f1"]) / metrics_a["macro_f1"]) * 100.0, 2)

    # 6. Save Model Artifact (Pipeline B)
    artifact_filename = f"{experiment_id}_{model_name}_{feature_type}.joblib"
    artifact_path = str(TRAINED_MODELS_DIR / artifact_filename)
    joblib.dump(pipeline_b, artifact_path)

    # Also save Model A artifact alongside
    joblib.dump(pipeline_a, str(TRAINED_MODELS_DIR / f"{experiment_id}_orig.joblib"))

    return {
        "original_train_size": len(X_train_orig),
        "augmented_train_size": len(X_train_augmented),
        "test_size": len(X_test),
        "artifact_path": artifact_path,
        "metrics_a": metrics_a,
        "metrics_b": metrics_b,
        "test_clauses": [{"text": txt, "label": lbl} for txt, lbl in zip(X_test, y_test)],
        "comparison": {
            "accuracy_delta": acc_delta,
            "macro_f1_delta": f1_delta,
            "weighted_f1_delta": weighted_f1_delta,
            "relative_f1_improvement_pct": rel_improvement,
            "performance_improved": f1_delta > 0
        }
    }

class ZeroLeakageExperiment:
    """
    Harness guaranteeing zero data leakage for both classification and regression.
    Separates test set BEFORE any data augmentation occurs.
    """
    def run_experiment(
        self,
        df,
        modality: str = "text",
        task_type: str = "classification",
        model_name: str = "logistic_regression",
        target_column: str = "category",
        input_column: str = "text",
        numerical_columns: list = None,
        algorithm: str = "synonym_replacement",
        test_size: float = 0.3,
        random_state: int = 42
    ):
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression, Ridge
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics import accuracy_score, f1_score, r2_score, mean_squared_error
        import pandas as pd

        if modality == "text":
            train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
            
            # Feature extraction strictly on train partition
            vec = TfidfVectorizer()
            X_train = vec.fit_transform(train_df[input_column])
            X_test = vec.transform(test_df[input_column])
            y_train = train_df[target_column]
            y_test = test_df[target_column]

            clf = LogisticRegression()
            clf.fit(X_train, y_train)
            preds_orig = clf.predict(X_test)
            acc_orig = float(accuracy_score(y_test, preds_orig))

            # Augment strictly train partition
            from backend.app.algorithms.synonym_replacement import SynonymReplacementAugmenter
            aug = SynonymReplacementAugmenter()
            aug_texts = [aug.augment(t) for t in train_df[input_column]]
            
            combined_texts = list(train_df[input_column]) + aug_texts
            combined_y = list(y_train) + list(y_train)
            
            vec_aug = TfidfVectorizer()
            X_train_aug = vec_aug.fit_transform(combined_texts)
            X_test_aug = vec_aug.transform(test_df[input_column])

            clf_aug = LogisticRegression()
            clf_aug.fit(X_train_aug, combined_y)
            preds_aug = clf_aug.predict(X_test_aug)
            acc_aug = float(accuracy_score(y_test, preds_aug))

            return {
                "zero_leakage_guaranteed": True,
                "baseline_metrics": {"accuracy": acc_orig},
                "augmented_metrics": {"accuracy": acc_aug},
                "gain_summary": {"accuracy_delta": acc_aug - acc_orig}
            }
        else:
            # Tabular
            num_cols = numerical_columns or [c for c in df.columns if c != target_column]
            train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
            
            X_train = train_df[num_cols]
            y_train = train_df[target_column]
            X_test = test_df[num_cols]
            y_test = test_df[target_column]

            reg = Ridge()
            reg.fit(X_train, y_train)
            preds_orig = reg.predict(X_test)
            r2_orig = float(r2_score(y_test, preds_orig))

            # Augment train
            from backend.app.algorithms.tabular_augmenter import TabularAugmenter
            tab_aug = TabularAugmenter()
            aug_train_df = tab_aug.inject_gaussian_noise(train_df, numerical_cols=num_cols, std_dev=0.05)
            combined_train = pd.concat([train_df, aug_train_df], ignore_index=True)

            reg_aug = Ridge()
            reg_aug.fit(combined_train[num_cols], combined_train[target_column])
            preds_aug = reg_aug.predict(X_test)
            r2_aug = float(r2_score(y_test, preds_aug))

            return {
                "zero_leakage_guaranteed": True,
                "baseline_metrics": {"r2": r2_orig},
                "augmented_metrics": {"r2": r2_aug},
                "gain_summary": {"r2_delta": r2_aug - r2_orig}
            }

