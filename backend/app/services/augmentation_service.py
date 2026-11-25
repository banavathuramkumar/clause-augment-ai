"""
Universal data augmentation service supporting:
- Text: EDA (Synonym replacement, insertion, deletion, swap), Sentence Restructuring, Gemini LLM Paraphrasing
- Tabular: Random Oversample, Bootstrap, SMOTE, Gaussian Noise, Numerical Perturbation, Categorical Resample
- Identifier Preservation: Auto-generates unique IDs for generated rows and keeps user-designated preserved columns intact.
"""
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
import uuid

from app.algorithms import (
    SynonymReplacer,
    RandomInserter,
    RandomDeleter,
    RandomSwapper,
    SentenceRestructurer,
    GeminiAugmenter,
    TabularAugmenter
)
from app.services.validation_service import ValidationService

class AugmentationService:
    def __init__(self):
        self.synonym_replacer = SynonymReplacer()
        self.random_inserter = RandomInserter()
        self.random_deleter = RandomDeleter()
        self.random_swapper = RandomSwapper()
        self.sentence_restructurer = SentenceRestructurer()
        self.gemini_augmenter = GeminiAugmenter()
        self.tabular_augmenter = TabularAugmenter()
        self.validator = ValidationService()

    def get_recommendations(self, stats: Dict[str, Any], modality: str = "text") -> List[Dict[str, Any]]:
        """Provides dynamic algorithmic augmentation recommendations based on data profile."""
        recs = []
        imbalance = stats.get("class_imbalance_ratio", 1.0)
        rows = stats.get("row_count", 0)

        if modality == "text":
            recs.append({
                "algorithm": "synonym_replacement",
                "suitability": "High",
                "reason": "Preserves core grammar while introducing domain-valid lexical diversity."
            })
            recs.append({
                "algorithm": "sentence_restructuring",
                "suitability": "High",
                "reason": "Syntactic transformation (voice/clause transposition) tests structural invariance."
            })
            recs.append({
                "algorithm": "random_swap",
                "suitability": "Medium",
                "reason": "Introduces robust noise to reduce overfitting on word orders."
            })
            if self.gemini_augmenter.is_available:
                recs.append({
                    "algorithm": "gemini_context_aware",
                    "suitability": "High",
                    "reason": "Contextual LLM paraphrasing provides natural semantic variations without keyword drift."
                })
        else: # tabular
            if imbalance > 1.5:
                recs.append({
                    "algorithm": "smote",
                    "suitability": "High",
                    "reason": f"Class imbalance detected (ratio: {imbalance:.2f}). SMOTE balances minority representations."
                })
                recs.append({
                    "algorithm": "random_oversample",
                    "suitability": "High",
                    "reason": "Oversamples minority classes with calibrated numerical jitter."
                })
            recs.append({
                "algorithm": "gaussian_noise",
                "suitability": "High",
                "reason": "Calibrated continuous perturbation smooths decision boundaries."
            })
            recs.append({
                "algorithm": "numerical_perturbation",
                "suitability": "Medium",
                "reason": "Bounded feature scaling preserves physical/domain constraints."
            })

        return recs

    def augment_text_row(
        self,
        text: str,
        algorithm: str = "synonym_replacement",
        num_variations: int = 1,
        validate: bool = True,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Generates augmented variants of a single text string."""
        results = []
        for _ in range(num_variations):
            if algorithm == "synonym_replacement":
                aug_text = self.synonym_replacer.augment(text, n_replacements=kwargs.get("n_replacements", 2))
            elif algorithm == "random_insertion":
                aug_text = self.random_inserter.augment(text, n_insertions=kwargs.get("n_insertions", 1))
            elif algorithm == "random_deletion":
                aug_text = self.random_deleter.augment(text, p=kwargs.get("p", 0.1))
            elif algorithm == "random_swap":
                aug_text = self.random_swapper.augment(text, n_swaps=kwargs.get("n_swaps", 1))
            elif algorithm == "sentence_restructuring":
                aug_text = self.sentence_restructurer.augment(text)
            elif algorithm == "gemini_context_aware":
                aug_text = self.gemini_augmenter.augment(text, domain_context=kwargs.get("domain", "general"))
            else:
                aug_text = self.synonym_replacer.augment(text)

            val_res = self.validator.validate_text_pair(text, aug_text) if validate else {
                "is_valid": True, "overall_score": 1.0, "similarity_score": 1.0, "flags": [], "rejection_reason": None
            }

            results.append({
                "original_text": text,
                "augmented_text": aug_text,
                "algorithm": algorithm,
                "validation": val_res
            })
        return results

    def augment_dataframe(
        self,
        df: pd.DataFrame,
        modality: str,
        input_column: Optional[str] = None,
        target_column: Optional[str] = None,
        id_column: Optional[str] = None,
        preserved_columns: Optional[List[str]] = None,
        algorithm: str = "synonym_replacement",
        num_variations: int = 1,
        validate: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """Universal dataframe augmentation pipeline."""
        augmented_records = []
        validation_summary = {"passed": 0, "failed": 0, "total": 0}

        if modality == "text" and input_column and input_column in df.columns:
            for idx, row in df.iterrows():
                orig_val = str(row[input_column])
                variants = self.augment_text_row(
                    text=orig_val,
                    algorithm=algorithm,
                    num_variations=num_variations,
                    validate=validate,
                    **kwargs
                )
                for v in variants:
                    aug_data = row.to_dict()
                    aug_data[input_column] = v["augmented_text"]
                    if id_column and id_column in aug_data:
                        aug_data[id_column] = f"aug_{uuid.uuid4().hex[:8]}"

                    val = v["validation"]
                    is_valid = val["is_valid"]
                    if is_valid:
                        validation_summary["passed"] += 1
                    else:
                        validation_summary["failed"] += 1
                    validation_summary["total"] += 1

                    augmented_records.append({
                        "original_data": row.to_dict(),
                        "augmented_data": aug_data,
                        "algorithm": algorithm,
                        "is_valid": is_valid,
                        "validation_score": val.get("overall_score", 1.0),
                        "rejection_reason": val.get("rejection_reason")
                    })

        elif modality == "tabular":
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if id_column and id_column in num_cols:
                num_cols.remove(id_column)
            if target_column and target_column in num_cols and kwargs.get("is_classification", True):
                num_cols.remove(target_column)

            cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
            if id_column and id_column in cat_cols:
                cat_cols.remove(id_column)
            if target_column and target_column in cat_cols:
                cat_cols.remove(target_column)

            if algorithm == "smote" and target_column:
                aug_df = self.tabular_augmenter.smote_oversample(
                    df=df, target_col=target_column, numerical_cols=num_cols, categorical_cols=cat_cols
                )
            elif algorithm == "random_oversample":
                aug_df = self.tabular_augmenter.random_oversample(
                    df=df, target_col=target_column, numerical_cols=num_cols
                )
            elif algorithm == "gaussian_noise":
                aug_df = self.tabular_augmenter.inject_gaussian_noise(
                    df=df, numerical_cols=num_cols, std_dev=kwargs.get("std_dev", 0.05)
                )
            elif algorithm == "numerical_perturbation":
                aug_df = self.tabular_augmenter.perturb_numerical(
                    df=df, numerical_cols=num_cols, perturbation_range=kwargs.get("range", 0.08)
                )
            elif algorithm == "resample_categorical":
                aug_df = self.tabular_augmenter.resample_categorical(
                    df=df, categorical_cols=cat_cols, mutation_rate=kwargs.get("mutation_rate", 0.1)
                )
            else:
                aug_df = self.tabular_augmenter.random_oversample(df=df, target_col=target_column, numerical_cols=num_cols)

            val_res = self.validator.validate_tabular(df, aug_df, numerical_cols=num_cols, categorical_cols=cat_cols)
            
            # Format rows
            for idx, row in aug_df.iterrows():
                aug_data = row.to_dict()
                if id_column and id_column in aug_data:
                    aug_data[id_column] = f"aug_{uuid.uuid4().hex[:8]}"

                is_valid = val_res["is_valid"]
                if is_valid:
                    validation_summary["passed"] += 1
                else:
                    validation_summary["failed"] += 1
                validation_summary["total"] += 1

                orig_sample = df.iloc[idx % len(df)].to_dict()
                augmented_records.append({
                    "original_data": orig_sample,
                    "augmented_data": aug_data,
                    "algorithm": algorithm,
                    "is_valid": is_valid,
                    "validation_score": 1.0 if is_valid else 0.5,
                    "rejection_reason": "; ".join(val_res["violations"]) if not is_valid else None
                })

        return {
            "augmented_records": augmented_records,
            "validation_summary": validation_summary,
            "total_generated": len(augmented_records)
        }
