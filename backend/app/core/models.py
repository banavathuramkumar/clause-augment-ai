import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    filename = Column(String(255), nullable=True)
    file_type = Column(String(32), default="csv")
    modality = Column(String(32), default="text")          # 'text', 'tabular', 'mixed'
    task_type = Column(String(32), default="classification") # 'classification', 'regression', 'unlabeled'
    total_rows = Column(Integer, default=0)
    total_columns = Column(Integer, default=0)
    input_column = Column(String(255), nullable=True)      # Primary text col or input feature summary
    target_column = Column(String(255), nullable=True)     # Target/label col (None if unlabeled)
    id_column = Column(String(255), nullable=True)         # Identifier column to preserve untouched
    columns_meta_json = Column(Text, default="[]")         # JSON list of columns metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    records = relationship("DatasetRecord", back_populates="dataset", cascade="all, delete-orphan")
    augmented_records = relationship("AugmentedRecord", back_populates="dataset", cascade="all, delete-orphan")
    experiments = relationship("TrainingExperiment", back_populates="dataset", cascade="all, delete-orphan")

class DatasetRecord(Base):
    __tablename__ = "dataset_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    row_index = Column(Integer, nullable=False)
    data_json = Column(Text, nullable=False)  # JSON representation of the complete row
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    dataset = relationship("Dataset", back_populates="records")
    augmented_records = relationship("AugmentedRecord", back_populates="original_record", cascade="all, delete-orphan")

class AugmentedRecord(Base):
    __tablename__ = "augmented_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    original_record_id = Column(String(36), ForeignKey("dataset_records.id"), nullable=True)
    technique = Column(String(64), nullable=False)
    original_data_json = Column(Text, nullable=False)
    augmented_data_json = Column(Text, nullable=False)
    status = Column(String(32), default="Pending")  # 'Pending', 'Accepted', 'Needs Review', 'Rejected'
    validation_reason = Column(Text, nullable=True)
    similarity_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    dataset = relationship("Dataset", back_populates="augmented_records")
    original_record = relationship("DatasetRecord", back_populates="augmented_records")
    validation_result = relationship("ValidationResult", uselist=False, back_populates="augmented_record", cascade="all, delete-orphan")

class ValidationResult(Base):
    __tablename__ = "validation_results"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    augmented_record_id = Column(String(36), ForeignKey("augmented_records.id"), nullable=False)
    similarity_score = Column(Float, nullable=False)
    constraints_preserved = Column(Boolean, default=True)
    status = Column(String(32), nullable=False)
    flag_reasons = Column(Text, default="[]")  # JSON encoded list of strings
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    augmented_record = relationship("AugmentedRecord", back_populates="validation_result")

class TrainingExperiment(Base):
    __tablename__ = "training_experiments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    name = Column(String(255), nullable=False)
    task_type = Column(String(32), default="classification") # 'classification' or 'regression'
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
    metrics_json = Column(Text, nullable=False)     # Complete metrics dictionary serialized as JSON
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    experiment = relationship("TrainingExperiment", back_populates="metrics")
