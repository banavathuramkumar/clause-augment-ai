# Milestone 12: Milestone 5 - Machine Learning Pipeline & Zero Leakage

## 1. Zero-Data-Leakage Protocol
To guarantee scientifically reproducible and leak-free results, the training pipeline enforces a strict 6-stage lifecycle:

```mermaid
flowchart LR
    A[Raw Dataset] -->|Split 80/20| B[Train Split]
    A -->|Split 80/20| C[Held-Out Test Split]
    B -->|Fit Vectorizer / Scaler| D[Train Transforms]
    D -->|Train Baseline Model| E[Baseline Model]
    B -->|Augment Train ONLY| F[Augmented Train Data]
    F -->|Transform via Pre-fitted Scaler| G[Augmented Transforms]
    G -->|Train Augmented Model| H[Augmented Model]
    C -->|Apply Pre-fitted Scaler| I[Unseen Test Set]
    E -->|Evaluate| J[Baseline Metrics]
    H -->|Evaluate| K[Augmented Metrics]
    J & K --> L[Statistical Comparison & Delta]
```

---

## 2. Supported Models & Tasks
- **Classification Tasks**:
  - `LogisticRegression`: High-interpretability generalized linear model with L2 regularization.
  - `LinearSVC`: Linear Support Vector Classifier suited for high-dimensional sparse TF-IDF spaces.
  - `MultinomialNB`: Fast Bayesian classification baseline.
  - `RandomForestClassifier`: Non-linear ensemble model for tabular and mixed features.
  - `DecisionTreeClassifier`: Transparent rule-based tree model.
- **Regression Tasks**:
  - `LinearRegression`: Ordinary least squares estimator.
  - `Ridge`: Regularized linear regression.
  - `RandomForestRegressor`: Ensemble regression for continuous target estimation.
