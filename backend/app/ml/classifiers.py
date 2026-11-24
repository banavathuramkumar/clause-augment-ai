from typing import Any
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

def get_classifier(model_name: str, random_state: int = 42) -> Any:
    if model_name == "LogisticRegression":
        return LogisticRegression(
            C=1.0,
            max_iter=1000,
            random_state=random_state,
            class_weight="balanced"
        )
    elif model_name == "MultinomialNB":
        return MultinomialNB(alpha=0.5)
    elif model_name == "LinearSVM":
        return LinearSVC(
            C=1.0,
            max_iter=2000,
            random_state=random_state,
            class_weight="balanced"
        )
    elif model_name == "RandomForest":
        return RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=random_state,
            class_weight="balanced"
        )
    else:
        raise ValueError(f"Unsupported model name: {model_name}")
