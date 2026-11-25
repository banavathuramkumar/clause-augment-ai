# Milestone 17: Test Cases & Empirical Results

## 1. Test Execution Matrix

| Test ID | Module Tested | Input Scenario | Expected Outcome | Status |
|---|---|---|---|---|
| **TC-01** | API Gateway | `GET /` & `GET /health` | Status 200, modalities `["text", "tabular"]` | **PASS** |
| **TC-02** | Text Augmentation | Legal clause + Synonym Replacement | Non-empty varied string; protected terms kept | **PASS** |
| **TC-03** | Gemini Augmenter | Missing API key | Clean fallback to sentence restructuring | **PASS** |
| **TC-04** | Tabular SMOTE | Imbalanced dataset (6 majority, 4 minority) | Minority class count equalized; numerical jitter applied | **PASS** |
| **TC-05** | Validation Cosine | High-similarity text pair | Score $> 0.60$, `is_valid == True` | **PASS** |
| **TC-06** | Validation Negation | Negation word inserted ("NOT") | Flag `NEGATION_MISMATCH`, rejected | **PASS** |
| **TC-07** | Zero-Leakage Split | Train/Test Split (80/20) | Preprocessor fitted exclusively on train | **PASS** |
| **TC-08** | Classification Eval | Baseline vs. Augmented LinearSVC | Accuracy & Macro F1 computed on held-out test split | **PASS** |
| **TC-09** | Regression Eval | Real Estate tabular Ridge regression | MAE, MSE, and $R^2$ computed on test set | **PASS** |
