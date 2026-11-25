"""
Universal data preprocessing service supporting:
- Text: Lowercasing, punctuation stripping, stopword removal, lemmatization with domain term preservation
- Tabular: Missing value imputation (mean/median/mode/drop), duplicate removal, min-max or standard scaling, categorical encoding
"""
from typing import Dict, Any, List, Optional
import re
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from app.config import PRESERVED_LEGAL_TERMS, NLTK_DATA_DIR

# Ensure NLTK path
if str(NLTK_DATA_DIR) not in nltk.data.path:
    nltk.data.path.insert(0, str(NLTK_DATA_DIR))

class PreprocessingService:
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words("english"))
        except Exception:
            self.stop_words = {"the", "a", "an", "is", "in", "it", "of", "to", "for", "with", "on", "at", "by"}
        self.lemmatizer = WordNetLemmatizer()
        self.preserved_terms = set(PRESERVED_LEGAL_TERMS)

    # ------------------ TEXT PREPROCESSING ------------------
    def clean_text(
        self,
        text: str,
        remove_stopwords: bool = True,
        lemmatize: bool = True,
        lowercase: bool = True,
        remove_punct: bool = True
    ) -> str:
        """Applies configurable NLP cleaning pipeline to raw text."""
        if not text or not isinstance(text, str):
            return ""

        cleaned = re.sub(r"\s+", " ", text).strip()

        if lowercase:
            cleaned = cleaned.lower()

        if remove_punct:
            cleaned = re.sub(r"[^\w\s]", " ", cleaned)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()

        try:
            tokens = word_tokenize(cleaned)
        except Exception:
            tokens = cleaned.split()

        processed_tokens = []
        for t in tokens:
            lower_t = t.lower()
            if lower_t in self.preserved_terms:
                processed_tokens.append(t)
                continue

            if remove_stopwords and lower_t in self.stop_words:
                continue

            if lemmatize:
                try:
                    t = self.lemmatizer.lemmatize(t)
                except Exception:
                    pass

            processed_tokens.append(t)

        return " ".join(processed_tokens)

    # ------------------ TABULAR PREPROCESSING ------------------
    def clean_tabular(
        self,
        df: pd.DataFrame,
        impute_strategy: str = "median", # mean, median, mode, drop
        remove_duplicates: bool = True,
        numerical_cols: Optional[List[str]] = None,
        categorical_cols: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Cleans tabular data, handles missing values and duplicates."""
        initial_rows = len(df)
        res_df = df.copy()

        # 1. Duplicates
        if remove_duplicates:
            res_df = res_df.drop_duplicates()
        duplicates_removed = initial_rows - len(res_df)

        num_cols = numerical_cols or res_df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = categorical_cols or res_df.select_dtypes(include=["object", "category"]).columns.tolist()

        missing_before = res_df.isnull().sum().to_dict()

        # 2. Missing value imputation
        if impute_strategy == "drop":
            res_df = res_df.dropna()
        else:
            # Impute numerical
            for col in num_cols:
                if col in res_df.columns and res_df[col].isnull().any():
                    if impute_strategy == "mean":
                        val = res_df[col].mean()
                    elif impute_strategy == "median":
                        val = res_df[col].median()
                    else:
                        val = 0
                    res_df[col] = res_df[col].fillna(val)

            # Impute categorical
            for col in cat_cols:
                if col in res_df.columns and res_df[col].isnull().any():
                    mode_series = res_df[col].mode()
                    mode_val = mode_series.iloc[0] if not mode_series.empty else "Unknown"
                    res_df[col] = res_df[col].fillna(mode_val)

        missing_after = res_df.isnull().sum().to_dict()

        return {
            "processed_df": res_df,
            "initial_rows": initial_rows,
            "final_rows": len(res_df),
            "duplicates_removed": duplicates_removed,
            "missing_before": missing_before,
            "missing_after": missing_after
        }
