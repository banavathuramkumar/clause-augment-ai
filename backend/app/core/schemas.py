"""
Pydantic schemas supporting universal datasets (text, tabular, mixed).
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

class ColumnMeta(BaseModel):
    name: str
    dtype: str
    role: str
    missing_count: int
    missing_ratio: float
    unique_count: int
    sample_values: List[Any]
    is_target_candidate: bool = False
    is_input_candidate: bool = False
    is_identifier: bool = False

class DatasetStats(BaseModel):
    row_count: int
    column_count: int
    modality: str
    task_type: str
    columns: List[ColumnMeta]
    missing_total: int
    duplicate_rows: int
    class_imbalance_ratio: Optional[float] = None
    target_distribution: Optional[Dict[str, int]] = None

class DatasetResponse(BaseModel):
    id: int
    name: str
    modality: str
    task_type: str
    row_count: int
    column_count: int
    input_column: Optional[str] = None
    target_column: Optional[str] = None
    id_column: Optional[str] = None
    preserved_columns: Optional[List[str]] = None
    columns_metadata: Optional[List[Dict[str, Any]]] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ColumnConfigUpdate(BaseModel):
    input_column: Optional[str] = None
    target_column: Optional[str] = None
    id_column: Optional[str] = None
    preserved_columns: Optional[List[str]] = None
    modality: Optional[str] = None
    task_type: Optional[str] = None

class AugmentationGenerateRequest(BaseModel):
    dataset_id: int
    algorithm: str
    num_variations: int = 1
    validate_augmented: bool = True
    hyperparameters: Optional[Dict[str, Any]] = Field(default_factory=dict)

class TrainingRequest(BaseModel):
    dataset_id: int
    model_name: str
    algorithm: str = "synonym_replacement"
    test_size: float = 0.2

class ExperimentResponse(BaseModel):
    experiment_id: Optional[int] = None
    model_name: str
    modality: str
    task_type: str
    algorithm: str
    train_size_original: int
    train_size_augmented: int
    test_size: int
    baseline_metrics: Dict[str, Any]
    augmented_metrics: Dict[str, Any]
    gain_summary: Dict[str, Any]
    zero_leakage_guaranteed: bool


class DatasetExpansionSummary(BaseModel):
    original_count: int
    augmented_count: int
    accepted_count: int
    rejected_count: int
    needs_review_count: int = 0
    expansion_percentage: float
    original_distribution: Optional[Dict[str, int]] = None
    augmented_distribution: Optional[Dict[str, int]] = None
