"""
Universal feature extraction pipeline for Text (TF-IDF) and Tabular (StandardScaler + OneHotEncoder).
Strictly fits on training split only to avoid data leakage.
"""
from typing import List, Optional
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

def create_text_pipeline(max_features: int = 3000, ngram_range=(1, 2)):
    """Returns a TF-IDF text vectorizer."""
    return TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        sublinear_tf=True
    )

def create_tabular_pipeline(
    numerical_cols: List[str],
    categorical_cols: List[str]
) -> ColumnTransformer:
    """Creates a scikit-learn ColumnTransformer for mixed tabular datasets."""
    transformers = []

    if numerical_cols:
        num_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])
        transformers.append(("num", num_pipe, numerical_cols))

    if categorical_cols:
        cat_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ])
        transformers.append(("cat", cat_pipe, categorical_cols))

    return ColumnTransformer(transformers=transformers, remainder="drop")
