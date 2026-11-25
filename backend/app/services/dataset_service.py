import io
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.config import DATASETS_DIR
from app.core.models import Dataset, DatasetRecord, AugmentedRecord
from app.core.schemas import DatasetStats, ColumnMeta, DatasetExpansionSummary
from app.utils.logger import logger

class DatasetService:
    @staticmethod
    def profile_dataframe(df: pd.DataFrame, custom_target: str = None, custom_input: str = None) -> Tuple[List[ColumnMeta], str, str, Optional[str], Optional[str], Optional[str]]:
        """
        Universally profiles any dataframe regardless of domain, column names, or data types.
        Returns: (columns_meta, modality, task_type, input_col, target_col, id_col)
        """
        columns_meta = []
        n_rows = len(df)
        
        detected_text_cols = []
        detected_num_cols = []
        detected_cat_cols = []
        detected_id_col = None

        for col in df.columns:
            series = df[col]
            missing_count = int(series.isna().sum())
            missing_pct = round((missing_count / max(1, n_rows)) * 100.0, 2)
            unique_count = int(series.nunique())
            sample_vals = series.dropna().head(3).tolist()
            # Convert non-serializable samples
            sample_vals = [str(v) if isinstance(v, (np.generic, pd.Timestamp)) else v for v in sample_vals]

            col_lower = str(col).lower()
            dtype_str = str(series.dtype)

            # 1. Identifier detection
            is_id = False
            if (any(x in col_lower for x in ["id", "code", "uuid", "guid", "key", "index"]) or 
                (unique_count == n_rows and n_rows > 10 and not pd.api.types.is_float_dtype(series))):
                detected_type = "identifier"
                is_id = True
                if not detected_id_col:
                    detected_id_col = col

            # 2. Numerical detection
            elif pd.api.types.is_numeric_dtype(series):
                if unique_count <= 5 and unique_count < n_rows * 0.05 and not pd.api.types.is_float_dtype(series):
                    detected_type = "categorical"
                    detected_cat_cols.append(col)
                else:
                    detected_type = "numerical"
                    detected_num_cols.append(col)

            # 3. Text vs Categorical detection
            else:
                str_series = series.dropna().astype(str)
                avg_words = float(str_series.apply(lambda s: len(s.split())).mean()) if len(str_series) > 0 else 0
                max_len = int(str_series.apply(len).max()) if len(str_series) > 0 else 0

                if avg_words > 3.0 or max_len > 35:
                    detected_type = "text"
                    detected_text_cols.append(col)
                elif unique_count <= 30 or unique_count <= max(5, int(n_rows * 0.15)):
                    detected_type = "categorical"
                    detected_cat_cols.append(col)
                else:
                    detected_type = "text"
                    detected_text_cols.append(col)

            columns_meta.append(ColumnMeta(
                name=str(col),
                dtype=dtype_str,
                detected_type=detected_type,
                missing_count=missing_count,
                missing_percentage=missing_pct,
                unique_count=unique_count,
                sample_values=sample_vals,
                is_id=is_id,
                is_preserved=is_id
            ))

        # Determine target column candidate
        target_candidate = custom_target
        if not target_candidate:
            target_keywords = ["label", "target", "class", "type", "category", "sentiment", "risk", "status", "default", "price", "outcome"]
            for col in df.columns:
                c_low = col.lower()
                if any(kw == c_low or f"_{kw}" in c_low or f"{kw}_" in c_low for kw in target_keywords):
                    target_candidate = col
                    break

        # Determine input column candidate
        input_candidate = custom_input
        if not input_candidate:
            if detected_text_cols:
                input_candidate = detected_text_cols[0]
            elif detected_num_cols:
                input_candidate = detected_num_cols[0]

        # Determine modality
        if detected_text_cols and (detected_num_cols or detected_cat_cols):
            modality = "text" if len(detected_text_cols) >= 1 and not detected_num_cols else "mixed"
        elif detected_text_cols:
            modality = "text"
        else:
            modality = "tabular"

        # Determine task type
        task_type = "unlabeled"
        if target_candidate and target_candidate in df.columns:
            target_series = df[target_candidate]
            if pd.api.types.is_numeric_dtype(target_series) and target_series.nunique() > 15:
                task_type = "regression"
            else:
                task_type = "classification"

        # Mark flags in columns_meta
        for c_meta in columns_meta:
            if c_meta.name == target_candidate:
                c_meta.is_target = True
            if c_meta.name == input_candidate:
                c_meta.is_input = True
            if c_meta.name == detected_id_col:
                c_meta.is_id = True
                c_meta.is_preserved = True

        return columns_meta, modality, task_type, input_candidate, target_candidate, detected_id_col

    @staticmethod
    def get_dataset_stats(df: pd.DataFrame, columns_meta: List[ColumnMeta], modality: str, task_type: str, target_col: Optional[str]) -> DatasetStats:
        class_dist = None
        target_summary = None
        imbalance_ratio = 1.0
        recommendations = []

        if target_col and target_col in df.columns:
            if task_type == "classification":
                counts = df[target_col].value_counts().to_dict()
                class_dist = {str(k): int(v) for k, v in counts.items()}
                if len(counts) > 1:
                    max_c = max(counts.values())
                    min_c = min(counts.values())
                    imbalance_ratio = round(max_c / max(1, min_c), 2)
                    if imbalance_ratio > 2.0:
                        recommendations.append(f"Significant class imbalance ({imbalance_ratio}:1) detected. Synthetic minority oversampling recommended.")
            elif task_type == "regression":
                s = df[target_col].dropna()
                target_summary = {
                    "mean": round(float(s.mean()), 2),
                    "median": round(float(s.median()), 2),
                    "std": round(float(s.std()), 2),
                    "min": round(float(s.min()), 2),
                    "max": round(float(s.max()), 2)
                }

        # Deduplication check
        duplicate_rows = int(df.duplicated().sum())
        if duplicate_rows > 0:
            recommendations.append(f"{duplicate_rows} duplicate row(s) identified. Preprocessing deduplication recommended.")

        # Modality recommendations
        if modality == "text":
            recommendations.append("Unstructured text modality: NLP synonym replacement, sentence restructuring, or Gemini context paraphrasing recommended.")
        else:
            recommendations.append("Structured tabular modality: Gaussian perturbation, bootstrap resampling, or SMOTE feature balancing recommended.")

        return DatasetStats(
            total_rows=len(df),
            total_columns=len(df.columns),
            modality=modality,
            task_type=task_type,
            columns=columns_meta,
            duplicate_rows=duplicate_rows,
            class_distribution=class_dist,
            target_summary=target_summary,
            imbalance_ratio=imbalance_ratio,
            recommendations=recommendations
        )

    @staticmethod
    def parse_file(filename: str, contents: bytes) -> pd.DataFrame:
        fn_lower = filename.lower()
        if fn_lower.endswith(".csv"):
            return pd.read_csv(io.BytesIO(contents))
        elif fn_lower.endswith(".json"):
            try:
                data = json.loads(contents.decode("utf-8"))
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict):
                    # Check common container keys
                    for k in ["data", "records", "items", "clauses", "reviews"]:
                        if k in data and isinstance(data[k], list):
                            return pd.DataFrame(data[k])
                    return pd.DataFrame([data])
                return pd.DataFrame(data)
            except Exception as e:
                raise ValueError(f"Invalid JSON file format: {str(e)}")
        elif fn_lower.endswith(".jsonl"):
            lines = [json.loads(line) for line in contents.decode("utf-8").splitlines() if line.strip()]
            return pd.DataFrame(lines)
        elif fn_lower.endswith((".xlsx", ".xls")):
            return pd.read_excel(io.BytesIO(contents))
        else:
            raise ValueError(f"Unsupported file format: {filename}. Supported formats are CSV, JSON, JSONL, and XLSX.")

    @staticmethod
    def create_dataset_from_dataframe(
        db: Session,
        name: str,
        df: pd.DataFrame,
        description: Optional[str] = None,
        filename: Optional[str] = None,
        file_type: str = "csv",
        custom_input: Optional[str] = None,
        custom_target: Optional[str] = None,
        custom_id: Optional[str] = None
    ) -> Dataset:
        if df.empty:
            raise ValueError("Uploaded dataset is empty.")

        # Replace NaN with None for clean JSON serialization
        df_clean = df.replace({np.nan: None})

        cols_meta, modality, task_type, input_col, target_col, id_col = DatasetService.profile_dataframe(
            df, custom_target=custom_target, custom_input=custom_input
        )
        if custom_id:
            id_col = custom_id

        dataset = Dataset(
            name=name,
            description=description or f"{modality.capitalize()} dataset with {len(df)} rows across {len(df.columns)} columns.",
            filename=filename,
            file_type=file_type,
            modality=modality,
            task_type=task_type,
            total_rows=len(df),
            total_columns=len(df.columns),
            input_column=input_col,
            target_column=target_col,
            id_column=id_col,
            columns_meta_json=json.dumps([c.model_dump() for c in cols_meta])
        )
        db.add(dataset)
        db.flush()

        # Insert records into DatasetRecord table
        records_to_insert = []
        for idx, row in df_clean.iterrows():
            row_dict = row.to_dict()
            records_to_insert.append(DatasetRecord(
                dataset_id=dataset.id,
                row_index=idx,
                data_json=json.dumps(row_dict, default=str)
            ))

        db.bulk_save_objects(records_to_insert)
        db.commit()
        db.refresh(dataset)
        logger.info(f"Created universal dataset '{dataset.name}' (ID: {dataset.id}, modality: {dataset.modality}) with {len(df)} rows.")
        return dataset

    @staticmethod
    def update_column_config(db: Session, config: Any) -> Dataset:
        dataset = db.query(Dataset).filter(Dataset.id == config.dataset_id).first()
        if not dataset:
            raise ValueError(f"Dataset {config.dataset_id} not found.")

        if config.input_column is not None:
            dataset.input_column = config.input_column
        if config.target_column is not None:
            dataset.target_column = config.target_column
        if config.id_column is not None:
            dataset.id_column = config.id_column
        if config.modality is not None:
            dataset.modality = config.modality
        if config.task_type is not None:
            dataset.task_type = config.task_type

        # Re-profile columns if overrides provided
        if config.column_overrides and dataset.columns_meta_json:
            cols_meta = [ColumnMeta(**c) for c in json.loads(dataset.columns_meta_json)]
            for c in cols_meta:
                if c.name in config.column_overrides:
                    c.detected_type = config.column_overrides[c.name]
                c.is_input = (c.name == dataset.input_column)
                c.is_target = (c.name == dataset.target_column)
                c.is_id = (c.name == dataset.id_column)
                c.is_preserved = c.is_id
            dataset.columns_meta_json = json.dumps([c.model_dump() for c in cols_meta])

        db.commit()
        db.refresh(dataset)
        return dataset

    @staticmethod
    def load_built_in_benchmarks(db: Session):
        """Pre-seeds diverse multi-domain datasets (Legal text, E-commerce reviews, Tabular credit risk, Tabular real estate)."""
        benchmarks = [
            ("Legal Contract Clauses Benchmark", "sample_contract_clauses.csv", "Legal clause dataset with 200 clauses across 10 categories.", "text", "clause_text", "clause_type", "clause_id"),
            ("Customer Feedback & Sentiment", "customer_reviews.csv", "E-commerce product reviews with 3 sentiment classes.", "text", "review_text", "sentiment", "review_id"),
            ("Credit Risk & Loan Default", "credit_risk_tabular.csv", "Financial credit risk assessment dataset with numerical and categorical features.", "tabular", "annual_income", "default_risk", "applicant_id"),
            ("Property Valuation (Regression)", "house_prices_regression.csv", "Real estate housing features and valuation prices.", "tabular", "square_feet", "price_thousands", "property_id"),
            ("Clinical Notes (Unlabeled)", "clinical_notes_unlabeled.csv", "Healthcare clinical observation transcripts without labels.", "text", "clinical_notes", None, "note_id"),
        ]

        for name, filename, desc, mod, in_col, tgt_col, id_col in benchmarks:
            existing = db.query(Dataset).filter(Dataset.name == name).first()
            if existing:
                continue

            filepath = DATASETS_DIR / filename
            if not filepath.exists():
                from datasets.generate_sample_data import generate_customer_reviews, generate_credit_risk, generate_house_prices, generate_unlabeled_clinical_notes
                generate_customer_reviews()
                generate_credit_risk()
                generate_house_prices()
                generate_unlabeled_clinical_notes()

            if filepath.exists():
                df = pd.read_csv(filepath)
                DatasetService.create_dataset_from_dataframe(
                    db=db,
                    name=name,
                    df=df,
                    description=desc,
                    filename=filename,
                    file_type="csv",
                    custom_input=in_col,
                    custom_target=tgt_col,
                    custom_id=id_col
                )

    @staticmethod
    def get_expansion_summary(db: Session, dataset_id: str) -> DatasetExpansionSummary:
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            raise ValueError(f"Dataset {dataset_id} not found")

        orig_records = db.query(DatasetRecord).filter(DatasetRecord.dataset_id == dataset_id).all()
        aug_records = db.query(AugmentedRecord).filter(AugmentedRecord.dataset_id == dataset_id).all()

        orig_count = len(orig_records)
        aug_count = len(aug_records)

        accepted = sum(1 for a in aug_records if a.status == "Accepted")
        rejected = sum(1 for a in aug_records if a.status == "Rejected")
        needs_review = sum(1 for a in aug_records if a.status == "Needs Review")

        expansion_pct = round((accepted / max(1, orig_count)) * 100.0, 1)

        orig_dist: Dict[str, int] = {}
        aug_dist: Dict[str, int] = {}

        if dataset.target_column:
            for r in orig_records:
                d = json.loads(r.data_json)
                lbl = str(d.get(dataset.target_column, "Unknown"))
                orig_dist[lbl] = orig_dist.get(lbl, 0) + 1

            aug_dist = dict(orig_dist)
            for a in aug_records:
                if a.status == "Accepted":
                    d = json.loads(a.augmented_data_json)
                    lbl = str(d.get(dataset.target_column, "Unknown"))
                    aug_dist[lbl] = aug_dist.get(lbl, 0) + 1

        return DatasetExpansionSummary(
            original_count=orig_count,
            augmented_count=aug_count,
            accepted_count=accepted,
            rejected_count=rejected,
            needs_review_count=needs_review,
            expansion_percentage=expansion_pct,
            original_distribution=orig_dist if orig_dist else None,
            augmented_distribution=aug_dist if aug_dist else None
        )

dataset_service = DatasetService()
