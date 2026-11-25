"""
Model factory for classification and regression models.
"""
from sklearn.linear_model import LogisticRegression, Ridge, LinearRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier

def get_classifier(model_name: str, random_state: int = 42):
    """Instantiates a classification model by name."""
    models = {
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=random_state),
        "linear_svc": LinearSVC(max_iter=2000, random_state=random_state),
        "multinomial_nb": MultinomialNB(),
        "random_forest": RandomForestClassifier(n_estimators=100, random_state=random_state),
        "decision_tree": DecisionTreeClassifier(random_state=random_state)
    }
    return models.get(model_name.lower(), LogisticRegression(max_iter=1000, random_state=random_state))

def get_regressor(model_name: str, random_state: int = 42):
    """Instantiates a regression model by name."""
    models = {
        "linear_regression": LinearRegression(),
        "ridge": Ridge(alpha=1.0, random_state=random_state),
        "random_forest_regressor": RandomForestRegressor(n_estimators=100, random_state=random_state)
    }
    return models.get(model_name.lower(), Ridge(alpha=1.0, random_state=random_state))
