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
