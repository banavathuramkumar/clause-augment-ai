import csv
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
from sqlalchemy.orm import Session
from backend.app.config import DATASETS_DIR, ALLOWED_CLAUSE_CATEGORIES
from backend.app.core.models import Dataset, Clause, AugmentedClause
from backend.app.core.schemas import DatasetStats, DatasetExpansionSummary
from backend.app.utils.logger import logger

class DatasetService:
    @staticmethod
    def get_stats(clauses: List[Clause]) -> DatasetStats:
        if not clauses:
            return DatasetStats(
                total_clauses=0,
                num_categories=0,
                category_distribution={},
                avg_word_count=0.0,
                imbalance_ratio=1.0
            )

        dist: Dict[str, int] = {}
        total_words = 0
        for c in clauses:
            dist[c.clause_type] = dist.get(c.clause_type, 0) + 1
            total_words += len(c.clause_text.split())

        counts = list(dist.values())
        max_c = max(counts) if counts else 1
        min_c = min(counts) if counts else 1
        imbalance = round(max_c / max(1, min_c), 2)

        return DatasetStats(
            total_clauses=len(clauses),
            num_categories=len(dist),
            category_distribution=dist,
            avg_word_count=round(total_words / len(clauses), 1),
            imbalance_ratio=imbalance
        )

    @staticmethod
    def create_dataset_from_records(
        db: Session,
        name: str,
        records: List[Dict[str, str]],
        description: Optional[str] = None,
        filename: Optional[str] = None
    ) -> Dataset:
        # Validate columns
        required = {"clause_id", "clause_text", "clause_type"}
        cleaned_records = []
        seen_texts = set()

        for idx, r in enumerate(records):
            if not required.issubset(set(r.keys())):
                raise ValueError(f"Record at row {idx+1} is missing mandatory keys: {required - set(r.keys())}")

            c_id = str(r["clause_id"]).strip()
            c_text = str(r["clause_text"]).strip()
            c_type = str(r["clause_type"]).strip()

            if not c_id or not c_text or not c_type:
                # Skip invalid empty rows
                continue

            # Deduplication
            normalized_text = " ".join(c_text.lower().split())
            if normalized_text in seen_texts:
                continue
            seen_texts.add(normalized_text)

            cleaned_records.append({
                "clause_id": c_id,
                "clause_text": c_text,
                "clause_type": c_type
            })

        if not cleaned_records:
            raise ValueError("No valid, non-duplicate clauses found in dataset.")

        categories = {r["clause_type"] for r in cleaned_records}

        dataset = Dataset(
            name=name,
            description=description or f"Contract clause dataset containing {len(cleaned_records)} clauses.",
            filename=filename,
            total_clauses=len(cleaned_records),
            num_categories=len(categories)
        )
        db.add(dataset)
        db.flush()

        for r in cleaned_records:
            clause = Clause(
                dataset_id=dataset.id,
                clause_id=r["clause_id"],
                clause_text=r["clause_text"],
                clause_type=r["clause_type"]
            )
            db.add(clause)

        db.commit()
        db.refresh(dataset)
        logger.info(f"Created dataset '{dataset.name}' (ID: {dataset.id}) with {len(cleaned_records)} clauses.")
        return dataset

    @staticmethod
    def load_built_in_sample(db: Session) -> Dataset:
        existing = db.query(Dataset).filter(Dataset.name == "Contract Clause Benchmark Dataset").first()
        if existing:
            return existing

        csv_path = DATASETS_DIR / "sample_contract_clauses.csv"
        if not csv_path.exists():
            from backend.datasets.generate_sample_data import generate_datasets
            generate_datasets()

        records = []
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)

        return DatasetService.create_dataset_from_records(
            db=db,
            name="Contract Clause Benchmark Dataset",
            records=records,
            description="Built-in legal clause benchmark dataset covering 10 standard legal categories with 200 clauses.",
            filename="sample_contract_clauses.csv"
        )

    @staticmethod
    def get_expansion_summary(db: Session, dataset_id: str) -> DatasetExpansionSummary:
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            raise ValueError("Dataset not found")

        orig_clauses = db.query(Clause).filter(Clause.dataset_id == dataset_id).all()
        aug_clauses = db.query(AugmentedClause).filter(AugmentedClause.dataset_id == dataset_id).all()

        orig_count = len(orig_clauses)
        aug_count = len(aug_clauses)

        accepted = sum(1 for a in aug_clauses if a.status == "Accepted")
        rejected = sum(1 for a in aug_clauses if a.status == "Rejected")
        needs_review = sum(1 for a in aug_clauses if a.status == "Needs Review")

        expansion_pct = round((accepted / max(1, orig_count)) * 100.0, 1)

        orig_dist: Dict[str, int] = {}
        for c in orig_clauses:
            orig_dist[c.clause_type] = orig_dist.get(c.clause_type, 0) + 1

        aug_dist: Dict[str, int] = dict(orig_dist)
        for a in aug_clauses:
            if a.status == "Accepted":
                aug_dist[a.clause_type] = aug_dist.get(a.clause_type, 0) + 1

        return DatasetExpansionSummary(
            original_count=orig_count,
            augmented_count=aug_count,
            accepted_count=accepted,
            rejected_count=rejected,
            needs_review_count=needs_review,
            expansion_percentage=expansion_pct,
            original_distribution=orig_dist,
            augmented_distribution=aug_dist
        )

dataset_service = DatasetService()
