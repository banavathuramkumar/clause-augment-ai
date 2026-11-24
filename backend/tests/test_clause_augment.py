import pytest
from backend.app.main import app
from backend.app.utils.text_cleaner import clean_legal_text, normalize_unicode, clean_whitespace
from backend.app.algorithms.synonym_replacement import SynonymReplacementAugmenter
from backend.app.algorithms.random_insertion import RandomInsertionAugmenter
from backend.app.algorithms.random_swap import RandomSwapAugmenter
from backend.app.algorithms.random_deletion import RandomDeletionAugmenter
from backend.app.algorithms.sentence_restructuring import SentenceRestructuringAugmenter
from backend.app.algorithms.back_translation import BackTranslationAugmenter
from backend.app.services.validation_service import validation_engine
from backend.app.ml.experiment import run_comparative_experiment
from backend.app.ml.metrics import compute_all_metrics
from backend.app.services.preprocessing_service import PreprocessingService
from backend.app.core.schemas import PreprocessingRequest

# 1. Text Preprocessing Tests
def test_unicode_and_whitespace_cleaning():
    raw = "  The \u2018Party\u2019   shall   pay \u2014 immediately.\n\n "
    normalized = normalize_unicode(raw)
    cleaned = clean_whitespace(normalized)
    assert cleaned == "The 'Party' shall pay -- immediately."

def test_preprocessing_preserves_legal_terms_and_negations():
    clause = "The Receiving Party shall not disclose without prior written consent unless authorized."
    proc, tokens, sents, ops = clean_legal_text(clause, remove_stopwords=True, lemmatize=True, preserve_legal_terms=True)
    lower_tokens = [t.lower() for t in tokens]
    assert "shall" in lower_tokens
    assert "not" in lower_tokens
    assert "without" in lower_tokens
    assert "unless" in lower_tokens

# 2. Augmentation Algorithm Tests
def test_synonym_replacement_protects_legal_keywords():
    aug = SynonymReplacementAugmenter()
    clause = "The Receiving Party shall indemnify Customer against patent infringement."
    results = aug.generate(clause, n=3, seed=42)
    assert len(results) == 3
    for r in results:
        assert "indemnify" in r.lower()
        assert "shall" in r.lower()

def test_random_insertion_preserves_obligations():
    aug = RandomInsertionAugmenter()
    clause = "Customer shall pay all undisputed invoices within thirty (30) days."
    results = aug.generate(clause, n=2, seed=42)
    assert len(results) == 2
    for r in results:
        assert "shall" in r
        assert "thirty (30) days" in r or "(30)" in r

def test_random_swap_coordinate_terms():
    aug = RandomSwapAugmenter()
    clause = "Each party shall defend and indemnify against all losses and damages."
    results = aug.generate(clause, n=2, seed=42)
    assert len(results) == 2
    for r in results:
        assert "shall" in r

def test_random_deletion_never_removes_negations_or_modals():
    aug = RandomDeletionAugmenter()
    clause = "In no event shall either party hereby be liable for consequential damages."
    results = aug.generate(clause, n=3, seed=42)
    assert len(results) == 3
    for r in results:
        assert "no" in r.lower()
        assert "shall" in r.lower()
        assert "liable" in r.lower()

def test_sentence_restructuring():
    aug = SentenceRestructuringAugmenter()
    clause = "In the event that Buyer fails to pay, Seller may terminate."
    results = aug.generate(clause, n=1, seed=42)
    assert len(results) == 1
    assert results[0].startswith("If ")

def test_back_translation_handles_offline_gracefully():
    aug = BackTranslationAugmenter()
    clause = "The agreement shall be governed by Delaware law."
    results = aug.generate(clause, n=1, seed=42)
    assert len(results) == 1
    assert results[0] == clause

# 3. Semantic Validation Tests
def test_semantic_validation_negation_preservation():
    orig = "The recipient shall not disclose confidential records."
    aug_tampered = "The recipient shall disclose confidential records."
    res = validation_engine.validate(orig, aug_tampered)
    assert res["status"] == "Rejected"
    assert res["negation_preserved"] is False

def test_semantic_validation_numeric_preservation():
    orig = "Payment shall be rendered within thirty (30) days."
    aug_tampered = "Payment shall be rendered within sixty (60) days."
    res = validation_engine.validate(orig, aug_tampered)
    assert res["status"] == "Rejected"
    assert res["numbers_dates_preserved"] is False

def test_semantic_validation_duplicate_detection():
    orig = "This Agreement shall be governed by the laws of Texas."
    aug_dup = "This Agreement shall be governed by the laws of Texas."
    res = validation_engine.validate(orig, aug_dup)
    assert res["status"] == "Rejected"
    assert "Trivial duplicate" in res["reason"]

# 4. Zero Data Leakage & Machine Learning Pipeline Tests
def test_leakage_free_experiment_pipeline():
    mock_orig = [
        {"id": f"c_{i}", "clause_id": f"CLS-{i}", "clause_text": f"Confidentiality obligation agreement number {i} shall remain confidential.", "clause_type": "Confidentiality"}
        for i in range(10)
    ] + [
        {"id": f"t_{i}", "clause_id": f"TRM-{i}", "clause_type": "Termination", "clause_text": f"Either party may terminate this agreement upon notice {i}."}
        for i in range(10)
    ]
    
    mock_aug = [
        {"id": f"a_{i}", "original_clause_id": f"c_{i}", "clause_type": "Confidentiality", "status": "Accepted", "augmented_text": f"Confidentiality agreement variation {i} shall be kept confidential."}
        for i in range(10)
    ]

    exp_res = run_comparative_experiment(
        original_clauses=mock_orig,
        augmented_clauses=mock_aug,
        model_name="LogisticRegression",
        feature_type="tfidf_unigram",
        train_ratio=0.8,
        random_state=42,
        experiment_id="test_exp"
    )

    assert "metrics_a" in exp_res
    assert "metrics_b" in exp_res
    assert "comparison" in exp_res
    assert exp_res["test_size"] == 4
    assert exp_res["original_train_size"] == 16
    assert exp_res["metrics_a"]["accuracy"] >= 0.0
    assert exp_res["metrics_b"]["accuracy"] >= 0.0

# 5. Metrics Computation Tests
def test_metrics_computation():
    y_true = ["Confidentiality", "Termination", "Payment", "Payment"]
    y_pred = ["Confidentiality", "Termination", "Payment", "Termination"]
    labels = ["Confidentiality", "Termination", "Payment"]
    metrics = compute_all_metrics(y_true, y_pred, labels)
    assert metrics["accuracy"] == 0.75
    assert 0.0 <= metrics["macro_f1"] <= 1.0

# 6. Service / Direct Logic Endpoint Tests
def test_api_routes_import_and_registration():
    paths = list(app.openapi()["paths"].keys())
    assert "/api/health" in paths
    assert "/api/datasets" in paths
    assert "/api/preprocessing/run" in paths
    assert "/api/augmentation/generate" in paths
    assert "/api/training/run" in paths
    assert "/api/evaluation/{experiment_id}" in paths
    assert "/api/robustness/run" in paths
    assert "/api/export/{export_type}" in paths

def test_preprocessing_service_direct():
    req = PreprocessingRequest(
        text="Vendor shall indemnify Client against all third-party claims.",
        remove_stopwords=False,
        lemmatize=False,
        preserve_legal_terms=True
    )
    res = PreprocessingService.process_clause(req)
    assert res.token_count > 0
    assert "shall" in res.processed_text.lower()
    assert "indemnify" in res.processed_text.lower()

# 7. Edge Case Tests
def test_edge_cases_empty_and_short_clauses():
    aug = SynonymReplacementAugmenter()
    short_res = aug.generate("Shall pay.", n=1, seed=42)
    assert len(short_res) == 1
    assert "pay" in short_res[0].lower()
