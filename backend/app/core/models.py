import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    filename = Column(String(255), nullable=True)
    total_clauses = Column(Integer, default=0)
    num_categories = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    clauses = relationship("Clause", back_populates="dataset", cascade="all, delete-orphan")
    augmented_clauses = relationship("AugmentedClause", back_populates="dataset", cascade="all, delete-orphan")
    experiments = relationship("TrainingExperiment", back_populates="dataset", cascade="all, delete-orphan")

class Clause(Base):
    __tablename__ = "clauses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    clause_id = Column(String(64), nullable=False)
    clause_text = Column(Text, nullable=False)
    clause_type = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    dataset = relationship("Dataset", back_populates="clauses")
    augmented_clauses = relationship("AugmentedClause", back_populates="original_clause", cascade="all, delete-orphan")

class AugmentedClause(Base):
    __tablename__ = "augmented_clauses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    original_clause_id = Column(String(36), ForeignKey("clauses.id"), nullable=False)
    technique = Column(String(64), nullable=False)
    original_text = Column(Text, nullable=False)
    augmented_text = Column(Text, nullable=False)
    clause_type = Column(String(128), nullable=False)
    random_seed = Column(Integer, nullable=True)
    status = Column(String(32), default="Pending")  # Pending, Accepted, Needs Review, Rejected
    validation_reason = Column(Text, nullable=True)
    similarity_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    dataset = relationship("Dataset", back_populates="augmented_clauses")
    original_clause = relationship("Clause", back_populates="augmented_clauses")
    validation_result = relationship("ValidationResult", uselist=False, back_populates="augmented_clause", cascade="all, delete-orphan")

class ValidationResult(Base):
    __tablename__ = "validation_results"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    augmented_clause_id = Column(String(36), ForeignKey("augmented_clauses.id"), nullable=False)
    similarity_score = Column(Float, nullable=False)
    legal_keywords_preserved = Column(Boolean, default=True)
    negation_preserved = Column(Boolean, default=True)
    modal_verbs_preserved = Column(Boolean, default=True)
    numbers_dates_preserved = Column(Boolean, default=True)
    status = Column(String(32), nullable=False)
    flag_reasons = Column(Text, default="[]")  # JSON encoded list
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    augmented_clause = relationship("AugmentedClause", back_populates="validation_result")

class TrainingExperiment(Base):
    __tablename__ = "training_experiments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    name = Column(String(255), nullable=False)
    model_name = Column(String(64), nullable=False)
    feature_type = Column(String(64), nullable=False)
    train_ratio = Column(Float, default=0.8)
    random_state = Column(Integer, default=42)
    original_train_size = Column(Integer, default=0)
    augmented_train_size = Column(Integer, default=0)
    test_size = Column(Integer, default=0)
    model_artifact_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    dataset = relationship("Dataset", back_populates="experiments")
    metrics = relationship("ModelMetrics", back_populates="experiment", cascade="all, delete-orphan")

class ModelMetrics(Base):
    __tablename__ = "model_metrics"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    experiment_id = Column(String(36), ForeignKey("training_experiments.id"), nullable=False)
    condition = Column(String(64), nullable=False)  # 'Original' or 'Augmented'
    accuracy = Column(Float, nullable=False)
    macro_precision = Column(Float, nullable=False)
    macro_recall = Column(Float, nullable=False)
    macro_f1 = Column(Float, nullable=False)
    weighted_f1 = Column(Float, nullable=False)
    confusion_matrix_json = Column(Text, nullable=False)
    classification_report_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    experiment = relationship("TrainingExperiment", back_populates="metrics")
