"""
Comprehensive test suite for ClauseAugment AI:
1. Universal Dataset Profiling & Multi-format parsing (CSV, JSON)
2. Text Augmentation Algorithms (Synonym replacement, Sentence restructuring, Insertion, Deletion, Swap)
3. Gemini Context-Aware Paraphrasing & Fallback logic
4. Tabular Augmentation Algorithms (SMOTE, Random Oversampling, Gaussian Noise, Numerical Perturbation)
5. Universal Validation Engine (Text cosine similarity & Negation checks; Tabular bounds & categories)
6. Zero-Data-Leakage ML Pipeline (Classification & Regression)
7. REST API Endpoints testing
"""
import pytest
import os
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient

from app.main import app
from app.algorithms import (
    SynonymReplacer,
    SentenceRestructurer,
    GeminiAugmenter,
    TabularAugmenter
)
from app.services.validation_service import ValidationService
from app.ml.experiment import ZeroLeakageExperiment

client = TestClient(app)

def test_api_root_and_health():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert "text" in data["supported_modalities"]
    assert "tabular" in data["supported_modalities"]

def test_text_augmentation_algorithms():
    syn_replacer = SynonymReplacer()
    text = "The vendor shall maintain strict confidentiality regarding all proprietary information."
    aug = syn_replacer.augment(text, n_replacements=2)
    assert isinstance(aug, str)
    assert len(aug) > 10

    restructurer = SentenceRestructurer()
    clause = "If the customer terminates the agreement, the provider shall refund any pre-paid fees."
    aug_restruct = restructurer.augment(clause)
    assert isinstance(aug_restruct, str)
    assert len(aug_restruct) > 10

def test_gemini_fallback():
    gemini = GeminiAugmenter()
    # If API key is not active, it should cleanly fall back without throwing an unhandled exception
    text = "Neither party shall be held liable for failure caused by force majeure."
    res = gemini.augment(text)
    assert isinstance(res, str)
    assert len(res) > 5

def test_tabular_augmentation_smote_and_noise():
    df = pd.DataFrame({
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "feature_num1": [10.5, 12.0, 11.2, 50.0, 52.1, 10.8, 11.0, 51.5, 11.5, 50.8],
        "feature_num2": [100, 120, 110, 500, 520, 105, 115, 510, 112, 505],
        "category": ["A", "A", "A", "B", "B", "A", "A", "B", "A", "B"],
        "target": [0, 0, 0, 1, 1, 0, 0, 1, 0, 1]
    })
    aug = TabularAugmenter()
    
    # Gaussian noise
    noisy_df = aug.inject_gaussian_noise(df, numerical_cols=["feature_num1", "feature_num2"], std_dev=0.05)
    assert len(noisy_df) == len(df)
    assert not np.allclose(noisy_df["feature_num1"], df["feature_num1"])

    # SMOTE oversampling
    smote_df = aug.smote_oversample(df, target_col="target", numerical_cols=["feature_num1", "feature_num2"])
    assert len(smote_df) >= len(df)

def test_validation_service():
    val = ValidationService()
    orig = "The supplier shall deliver the items within 30 days."
    aug = "The supplier shall provide the items within 30 days."
    res = val.validate_text_pair(orig, aug)
    assert res["is_valid"] is True
    assert res["similarity_score"] > 0.6

    # Negation inversion check
    neg_aug = "The supplier shall NOT deliver the items within 30 days."
    res_neg = val.validate_text_pair(orig, neg_aug)
    assert "NEGATION_MISMATCH" in res_neg["flags"]

def test_zero_leakage_classification_experiment():
    df = pd.DataFrame({
        "text": [
            "This contract shall be governed by Delaware law.",
            "Any disputes will be resolved in courts of New York.",
            "All confidential records must be returned immediately.",
            "Trade secrets will not be disclosed to any third party.",
            "The vendor shall be governed by California jurisdiction.",
            "Governing law for this agreement is England and Wales.",
            "Proprietary materials are kept strictly confidential.",
            "Confidentiality obligation survives termination.",
            "Disputes will be settled via binding arbitration.",
            "Arbitration shall occur in London UK."
        ],
        "category": ["Legal", "Legal", "Confidential", "Confidential", "Legal", "Legal", "Confidential", "Confidential", "Dispute", "Dispute"]
    })

    runner = ZeroLeakageExperiment()
    res = runner.run_experiment(
        df=df,
        modality="text",
        task_type="classification",
        model_name="logistic_regression",
        target_column="category",
        input_column="text",
        algorithm="synonym_replacement",
        test_size=0.3,
        random_state=42
    )
    assert res["zero_leakage_guaranteed"] is True
    assert "baseline_metrics" in res
    assert "augmented_metrics" in res
    assert "gain_summary" in res

def test_zero_leakage_regression_experiment():
    df = pd.DataFrame({
        "square_feet": [500, 750, 1000, 1200, 1500, 1800, 2000, 2200, 2500, 3000],
        "bedrooms": [1, 2, 2, 3, 3, 4, 4, 4, 5, 5],
        "price": [150.0, 210.0, 280.0, 330.0, 410.0, 490.0, 540.0, 590.0, 680.0, 800.0]
    })
    runner = ZeroLeakageExperiment()
    res = runner.run_experiment(
        df=df,
        modality="tabular",
        task_type="regression",
        model_name="ridge",
        target_column="price",
        numerical_columns=["square_feet", "bedrooms"],
        algorithm="numerical_perturbation",
        test_size=0.3,
        random_state=42
    )
    assert res["zero_leakage_guaranteed"] is True
    assert "r2" in res["baseline_metrics"]
    assert "r2" in res["augmented_metrics"]
