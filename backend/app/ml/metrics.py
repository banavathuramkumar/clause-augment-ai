"""
Evaluation metrics computation for both classification and regression.
"""
from typing import Dict, Any, List
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

def compute_classification_metrics(y_true, y_pred, labels: List[str] = None) -> Dict[str, Any]:
    """Calculates accuracy, precision, recall, macro/weighted F1 and confusion matrix."""
    acc = float(accuracy_score(y_true, y_pred))
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
    p_wt, r_wt, f1_wt, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)

    unique_labels = labels if labels is not None else sorted(list(set(y_true).union(set(y_pred))))
    cm = confusion_matrix(y_true, y_pred, labels=unique_labels).tolist()

    report = classification_report(y_true, y_pred, labels=unique_labels, output_dict=True, zero_division=0)

    return {
        "accuracy": round(acc, 4),
        "macro_f1": round(float(f1_macro), 4),
        "weighted_f1": round(float(f1_wt), 4),
        "precision": round(float(p_weighted if 'p_weighted' in locals() else p_wt), 4),
        "recall": round(float(r_weighted if 'r_weighted' in locals() else r_wt), 4),
        "confusion_matrix": cm,
        "classes": [str(c) for c in unique_labels],
        "per_class_report": report
    }

def compute_regression_metrics(y_true, y_pred) -> Dict[str, Any]:
    """Calculates MAE, MSE, RMSE, and R2 for regression models."""
    mae = float(mean_absolute_error(y_true, y_pred))
    mse = float(mean_squared_error(y_true, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_true, y_pred))

    return {
        "mae": round(mae, 4),
        "mse": round(mse, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4)
    }
