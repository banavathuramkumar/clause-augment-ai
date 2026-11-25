from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# Dataset schemas
class ClauseBase(BaseModel):
    clause_id: str
    clause_text: str
    clause_type: str

class ClauseResponse(ClauseBase):
    id: str
    dataset_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DatasetStats(BaseModel):
    total_clauses: int
    num_categories: int
    category_distribution: Dict[str, int]
    avg_word_count: float
    imbalance_ratio: float  # max_count / min_count

class DatasetResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    filename: Optional[str] = None
    total_clauses: int
    num_categories: int
    created_at: datetime
    stats: Optional[DatasetStats] = None

    model_config = ConfigDict(from_attributes=True)

# Preprocessing schemas
class PreprocessingRequest(BaseModel):
    text: str
    remove_stopwords: bool = False
    lemmatize: bool = False
    preserve_legal_terms: bool = True

class PreprocessingResponse(BaseModel):
    original_text: str
    processed_text: str
    original_word_count: int
    processed_word_count: int
    token_count: int
    tokens: List[str]
    sentences: List[str]
    operations_applied: List[str]

# Augmentation schemas
class AugmentationGenerateRequest(BaseModel):
    dataset_id: str
    techniques: List[str] = Field(
        default=[
            "transformer_paraphrase",
            "nlpaug_synonym",
            "synonym_replacement",
            "random_insertion",
            "random_swap",
            "random_deletion",
            "sentence_restructuring"
        ]
    )
    multiplier: int = Field(default=1, ge=1, le=5)  # 1x, 2x, 3x, 5x
    selected_categories: Optional[List[str]] = None
    random_seed: int = 42
    similarity_threshold: float = Field(default=0.75, ge=0.5, le=1.0)
    auto_validate: bool = True
    # Transformer paraphrasing parameters
    temperature: Optional[float] = Field(default=0.7, ge=0.1, le=1.5)
    top_p: Optional[float] = Field(default=0.9, ge=0.1, le=1.0)
    repetition_penalty: Optional[float] = Field(default=1.2, ge=1.0, le=2.0)


class AugmentedClauseResponse(BaseModel):
    id: str
    dataset_id: str
    original_clause_id: str
    technique: str
    original_text: str
    augmented_text: str
    clause_type: str
    random_seed: Optional[int]
    status: str
    validation_reason: Optional[str]
    similarity_score: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AugmentationApprovalRequest(BaseModel):
    augmented_clause_ids: List[str]
    action: str = Field(..., pattern="^(approve|reject)$")
    reason: Optional[str] = None

# Validation schemas
class ValidationRunRequest(BaseModel):
    dataset_id: str
    similarity_threshold: float = 0.75
    enforce_negations: bool = True
    enforce_modal_verbs: bool = True
    enforce_keywords: bool = True
    enforce_numbers_dates: bool = True

class ValidationItemResult(BaseModel):
    id: str
    augmented_clause_id: str
    original_text: str
    augmented_text: str
    technique: str
    similarity_score: float
    legal_keywords_preserved: bool
    negation_preserved: bool
    modal_verbs_preserved: bool
    numbers_dates_preserved: bool
    status: str
    flag_reasons: List[str]

# Expansion schemas
class DatasetExpansionSummary(BaseModel):
    original_count: int
    augmented_count: int
    accepted_count: int
    rejected_count: int
    needs_review_count: int
    expansion_percentage: float
    original_distribution: Dict[str, int]
    augmented_distribution: Dict[str, int]

# Training & ML schemas
class TrainingRunRequest(BaseModel):
    dataset_id: str
    model_name: str = Field(default="LogisticRegression", pattern="^(LogisticRegression|MultinomialNB|LinearSVM|RandomForest)$")
    feature_type: str = Field(default="tfidf_unigram", pattern="^(tfidf_unigram|tfidf_bigram)$")
    train_ratio: float = Field(default=0.8, ge=0.5, le=0.9)
    random_state: int = 42
    use_approved_only: bool = True

class MetricsDetail(BaseModel):
    condition: str
    accuracy: float
    macro_precision: float
    macro_recall: float
    macro_f1: float
    weighted_f1: float
    confusion_matrix: List[List[int]]
    labels: List[str]
    classification_report: Dict[str, Any]

class ExperimentResponse(BaseModel):
    id: str
    dataset_id: str
    name: str
    model_name: str
    feature_type: str
    train_ratio: float
    random_state: int
    original_train_size: int
    augmented_train_size: int
    test_size: int
    created_at: datetime
    metrics: Dict[str, MetricsDetail]
    comparison: Dict[str, Any]

# Robustness Testing schemas
class RobustnessRunRequest(BaseModel):
    experiment_id: str
    perturbation_types: List[str] = Field(
        default=["paraphrase_stress", "drafting_style_shift", "punctuation_spacing", "case_typo"]
    )

class RobustnessResult(BaseModel):
    perturbation_type: str
    original_model_accuracy: float
    augmented_model_accuracy: float
    original_model_f1: float
    augmented_model_f1: float
    accuracy_delta: float
    f1_delta: float
    robustness_gain: float
    sample_perturbations: List[Dict[str, str]]
