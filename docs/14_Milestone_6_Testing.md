# Milestone 14: Milestone 6 - Testing & Verification

## 1. Testing Framework & Methodology
The test suite in `backend/tests/test_clause_augment.py` covers end-to-end integration and algorithmic unit tests:
- **API Endpoint Verification**: Tests the `/` root and `/health` endpoints to confirm OpenAPI documentation generation and supported modality declarations (`text`, `tabular`).
- **Text Augmentation Verification**: Confirms WordNet synonym replacement and syntactic clause inversion generate non-empty, valid variations.
- **Gemini Fallback Logic**: Verifies that when `GEMINI_API_KEY` is not present or blocked, the service gracefully falls back to deterministic local sentence restructuring without raising exceptions.
- **Tabular SMOTE and Noise**: Confirms Gaussian noise introduces expected variance to numerical features and SMOTE restores balance to minority classes.
- **Validation Engine**: Confirms cosine similarity checks accept valid paraphrases while detecting semantic violations such as negation inversions.
- **Zero-Leakage Training Pipeline**: Evaluates classification and regression experiments on isolated splits, ensuring no test data leaks into the vectorizers or models.
