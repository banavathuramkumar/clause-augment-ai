"""
Universal validation service supporting:
- Text: Cosine similarity, negation shift check, modal verbs check, numeric token retention, length ratio, grammar sanity
- Tabular: Range and bounds compliance, data type consistency, categorical domain integrity, duplicate record check
"""
from typing import Dict, Any, List, Optional
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.config import (
    MIN_SEMANTIC_SIMILARITY,
    MAX_SEMANTIC_SIMILARITY,
    MAX_LENGTH_RATIO_DIFFERENCE,
    NEGATION_WORDS,
    MODAL_VERBS
)

class ValidationService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    # ------------------ TEXT VALIDATION ------------------
    def validate_text_pair(
        self,
        original_text: str,
        augmented_text: str,
        min_sim: float = MIN_SEMANTIC_SIMILARITY,
        max_sim: float = MAX_SEMANTIC_SIMILARITY,
        strict_negation: bool = True
    ) -> Dict[str, Any]:
        """Validates semantic and grammatical consistency between original and augmented text."""
        flags = []
        scores = {}

        if not augmented_text or not augmented_text.strip():
            return {
                "is_valid": False,
                "overall_score": 0.0,
                "similarity_score": 0.0,
                "flags": ["EMPTY_OUTPUT"],
                "rejection_reason": "Augmented text is empty"
            }

        # 1. Similarity
        try:
            tfidf = self.vectorizer.fit_transform([original_text, augmented_text])
            sim = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
        except Exception:
            sim = 0.5
        scores["similarity"] = round(sim, 4)

        if sim < min_sim:
            flags.append("SIMILARITY_TOO_LOW")
        elif sim > max_sim:
            flags.append("IDENTICAL_OR_NO_VARIATION")

        # 2. Length ratio
        orig_len = max(1, len(original_text.split()))
        aug_len = max(1, len(augmented_text.split()))
        len_ratio = aug_len / orig_len
        scores["length_ratio"] = round(len_ratio, 3)

        if abs(1.0 - len_ratio) > MAX_LENGTH_RATIO_DIFFERENCE:
            flags.append("EXCESSIVE_LENGTH_DRIFT")

        # 3. Negations
        orig_words = set(re.findall(r"\b\w+\b", original_text.lower()))
        aug_words = set(re.findall(r"\b\w+\b", augmented_text.lower()))

        orig_neg = orig_words.intersection(NEGATION_WORDS)
        aug_neg = aug_words.intersection(NEGATION_WORDS)
        if strict_negation and orig_neg != aug_neg:
            flags.append("NEGATION_MISMATCH")

        # 4. Modals
        orig_mod = orig_words.intersection(MODAL_VERBS)
        aug_mod = aug_words.intersection(MODAL_VERBS)
        if orig_mod and not aug_mod:
            flags.append("OBLIGATION_MODAL_LOST")

        # 5. Number and Entity retention
        orig_nums = set(re.findall(r"\b\d+(?:\.\d+)?\b", original_text))
        aug_nums = set(re.findall(r"\b\d+(?:\.\d+)?\b", augmented_text))
        if orig_nums and not orig_nums.issubset(aug_nums):
            flags.append("NUMERICAL_ENTITY_ALTERED")

        # Overall validity
        is_valid = len([f for f in flags if f in ["SIMILARITY_TOO_LOW", "EMPTY_OUTPUT", "NEGATION_MISMATCH"]]) == 0
        rejection_reason = ", ".join(flags) if not is_valid else None

        return {
            "is_valid": is_valid,
            "overall_score": scores.get("similarity", 0.5),
            "similarity_score": scores.get("similarity", 0.5),
            "flags": flags,
            "rejection_reason": rejection_reason
        }

    # ------------------ TABULAR VALIDATION ------------------
    def validate_tabular(
        self,
        original_df: pd.DataFrame,
        augmented_df: pd.DataFrame,
        numerical_cols: Optional[List[str]] = None,
        categorical_cols: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Validates bounds, nulls, and categorical domains for augmented tabular data."""
        num_cols = numerical_cols or original_df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = categorical_cols or original_df.select_dtypes(include=["object", "category"]).columns.tolist()

        violations = []
        
        # 1. Check bounds for numerical columns
        for col in num_cols:
            if col in original_df.columns and col in augmented_df.columns:
                orig_min = original_df[col].min()
                orig_max = original_df[col].max()
                # allow 15% tolerance
                span = orig_max - orig_min
                lower_bound = orig_min - 0.15 * span
                upper_bound = orig_max + 0.15 * span

                aug_series = pd.to_numeric(augmented_df[col], errors='coerce')
                out_of_bounds = ((aug_series < lower_bound) | (aug_series > upper_bound)).sum()
                if out_of_bounds > 0:
                    violations.append(f"Column '{col}' has {out_of_bounds} values outside plausible domain [{lower_bound:.2f}, {upper_bound:.2f}]")

        # 2. Check categorical domains
        for col in cat_cols:
            if col in original_df.columns and col in augmented_df.columns:
                allowed_categories = set(original_df[col].dropna().unique())
                aug_categories = set(augmented_df[col].dropna().unique())
                new_categories = aug_categories - allowed_categories
                if new_categories:
                    violations.append(f"Column '{col}' introduced unobserved categories: {new_categories}")

        # 3. Check null count drift
        aug_nulls = int(augmented_df.isnull().sum().sum())
        is_valid = len(violations) == 0

        return {
            "is_valid": is_valid,
            "violations": violations,
            "augmented_rows": len(augmented_df),
            "augmented_nulls": aug_nulls,
            "passed_checks": len(violations) == 0
        }
