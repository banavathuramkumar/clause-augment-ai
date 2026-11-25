import os
import io
import csv
import json
import joblib
from typing import Dict, Any, List, Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from app.core.models import Dataset, Clause, AugmentedClause, TrainingExperiment, ModelMetrics
from app.config import EXPORTS_DIR, TRAINED_MODELS_DIR

class ExportService:
    @staticmethod
    def export_clauses_csv(db: Session, dataset_id: str, kind: str = "original") -> str:
        """kind: 'original', 'augmented', 'accepted', 'rejected'"""
        filepath = EXPORTS_DIR / f"{dataset_id}_{kind}_clauses.csv"
        
        if kind == "original":
            clauses = db.query(Clause).filter(Clause.dataset_id == dataset_id).all()
            with open(filepath, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["clause_id", "clause_text", "clause_type", "created_at"])
                writer.writeheader()
                for c in clauses:
                    writer.writerow({
                        "clause_id": c.clause_id,
                        "clause_text": c.clause_text,
                        "clause_type": c.clause_type,
                        "created_at": c.created_at.isoformat() if c.created_at else ""
                    })
        else:
            q = db.query(AugmentedClause).filter(AugmentedClause.dataset_id == dataset_id)
            if kind == "accepted":
                q = q.filter(AugmentedClause.status == "Accepted")
            elif kind == "rejected":
                q = q.filter(AugmentedClause.status == "Rejected")
            clauses = q.all()
            with open(filepath, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "id", "original_clause_id", "technique", "original_text",
                    "augmented_text", "clause_type", "status", "similarity_score",
                    "validation_reason", "created_at"
                ])
                writer.writeheader()
                for c in clauses:
                    writer.writerow({
                        "id": c.id,
                        "original_clause_id": c.original_clause_id,
                        "technique": c.technique,
                        "original_text": c.original_text,
                        "augmented_text": c.augmented_text,
                        "clause_type": c.clause_type,
                        "status": c.status,
                        "similarity_score": c.similarity_score,
                        "validation_reason": c.validation_reason or "",
                        "created_at": c.created_at.isoformat() if c.created_at else ""
                    })

        return str(filepath)

    @staticmethod
    def export_dataset_json(db: Session, dataset_id: str) -> str:
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            raise ValueError("Dataset not found")

        clauses = db.query(Clause).filter(Clause.dataset_id == dataset_id).all()
        augmented = db.query(AugmentedClause).filter(AugmentedClause.dataset_id == dataset_id).all()

        data = {
            "dataset_info": {
                "id": dataset.id,
                "name": dataset.name,
                "total_clauses": dataset.total_clauses,
                "num_categories": dataset.num_categories,
                "created_at": dataset.created_at.isoformat() if dataset.created_at else ""
            },
            "original_clauses": [
                {"clause_id": c.clause_id, "clause_text": c.clause_text, "clause_type": c.clause_type}
                for c in clauses
            ],
            "augmented_clauses": [
                {
                    "id": a.id,
                    "original_clause_id": a.original_clause_id,
                    "technique": a.technique,
                    "augmented_text": a.augmented_text,
                    "clause_type": a.clause_type,
                    "status": a.status,
                    "similarity_score": a.similarity_score
                }
                for a in augmented
            ]
        }

        filepath = EXPORTS_DIR / f"{dataset_id}_dataset.json"
        with open(filepath, mode="w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return str(filepath)

    @staticmethod
    def export_classification_report_csv(db: Session, experiment_id: str) -> str:
        metrics = db.query(ModelMetrics).filter(ModelMetrics.experiment_id == experiment_id).all()
        filepath = EXPORTS_DIR / f"{experiment_id}_classification_report.csv"

        rows = []
        for m in metrics:
            rep = json.loads(m.classification_report_json)
            for label, scores in rep.items():
                if isinstance(scores, dict):
                    rows.append({
                        "condition": m.condition,
                        "class_label": label,
                        "precision": scores.get("precision", 0),
                        "recall": scores.get("recall", 0),
                        "f1-score": scores.get("f1-score", 0),
                        "support": scores.get("support", 0)
                    })

        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["condition", "class_label", "precision", "recall", "f1-score", "support"])
            writer.writeheader()
            writer.writerows(rows)

        return str(filepath)

    @staticmethod
    def generate_confusion_matrix_image(db: Session, experiment_id: str) -> str:
        metrics = db.query(ModelMetrics).filter(ModelMetrics.experiment_id == experiment_id).all()
        if not metrics:
            raise ValueError("No metrics found for experiment")

        filepath = EXPORTS_DIR / f"{experiment_id}_confusion_matrices.png"

        fig, axes = plt.subplots(1, len(metrics), figsize=(7 * len(metrics), 6))
        if len(metrics) == 1:
            axes = [axes]

        for ax, m in zip(axes, metrics):
            cm = json.loads(m.confusion_matrix_json)
            rep = json.loads(m.classification_report_json)
            labels = [k for k in rep.keys() if k not in {"accuracy", "macro avg", "weighted avg"}]
            short_labels = [l[:10] for l in labels]

            sns.heatmap(
                cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=short_labels, yticklabels=short_labels, ax=ax
            )
            ax.set_title(f"{m.condition} (Acc: {m.accuracy*100:.1f}%, F1: {m.macro_f1:.3f})")
            ax.set_xlabel("Predicted")
            ax.set_ylabel("True")

        plt.tight_layout()
        plt.savefig(filepath, dpi=200)
        plt.close(fig)

        return str(filepath)

    @staticmethod
    def generate_evaluation_report_pdf(db: Session, experiment_id: str) -> str:
        exp = db.query(TrainingExperiment).filter(TrainingExperiment.id == experiment_id).first()
        if not exp:
            raise ValueError("Experiment not found")

        metrics = db.query(ModelMetrics).filter(ModelMetrics.experiment_id == experiment_id).all()
        filepath = EXPORTS_DIR / f"{experiment_id}_evaluation_report.pdf"

        doc = SimpleDocTemplate(str(filepath), pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Heading1"],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0f172a"),
            alignment=1
        )
        story.append(Paragraph("ClauseAugment AI – Evaluation Report", title_style))
        story.append(Spacer(1, 10))

        subtitle = f"Experiment ID: {exp.id}<br/>Model: {exp.model_name} | Feature: {exp.feature_type} | Date: {exp.created_at.strftime('%Y-%m-%d %H:%M:%S') if exp.created_at else ''}"
        story.append(Paragraph(subtitle, styles["Normal"]))
        story.append(Spacer(1, 15))

        # Dataset partition summary
        part_data = [
            ["Metric / Split", "Original Baseline (Exp A)", "Augmented Pipeline (Exp B)", "Delta / Gain"],
            ["Train Clause Count", str(exp.original_train_size), str(exp.augmented_train_size), f"+{exp.augmented_train_size - exp.original_train_size}"],
            ["Held-Out Test Size", str(exp.test_size), str(exp.test_size), "Identical Partition (Zero Leakage)"]
        ]
        
        m_dict = {m.condition: m for m in metrics}
        m_a = m_dict.get("Original")
        m_b = m_dict.get("Augmented")

        if m_a and m_b:
            part_data.extend([
                ["Test Accuracy", f"{m_a.accuracy * 100:.2f}%", f"{m_b.accuracy * 100:.2f}%", f"{(m_b.accuracy - m_a.accuracy)*100:+.2f}%"],
                ["Macro Precision", f"{m_a.macro_precision:.4f}", f"{m_b.macro_precision:.4f}", f"{m_b.macro_precision - m_a.macro_precision:+.4f}"],
                ["Macro Recall", f"{m_a.macro_recall:.4f}", f"{m_b.macro_recall:.4f}", f"{m_b.macro_recall - m_a.macro_recall:+.4f}"],
                ["Macro F1-Score", f"{m_a.macro_f1:.4f}", f"{m_b.macro_f1:.4f}", f"{m_b.macro_f1 - m_a.macro_f1:+.4f}"],
                ["Weighted F1-Score", f"{m_a.weighted_f1:.4f}", f"{m_b.weighted_f1:.4f}", f"{m_b.weighted_f1 - m_a.weighted_f1:+.4f}"]
            ])

        t = Table(part_data, colWidths=[150, 130, 130, 130])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("FONTSIZE", (0, 0), (-1, -1), 9)
        ]))
        story.append(t)
        story.append(Spacer(1, 20))

        story.append(Paragraph("<b>Methodology & Leakage Prevention:</b>", styles["Heading3"]))
        methodology_text = (
            "The evaluation strictly enforces data segregation. The original corpus was partitioned into training and held-out test splits. "
            "Data augmentation was applied exclusively to the training subset. Feature vectorizers were fitted strictly on training data without exposure to test clauses. "
            "Both models were evaluated on the exact same unseen original test set to ensure rigorous comparative scientific assessment."
        )
        story.append(Paragraph(methodology_text, styles["Normal"]))

        doc.build(story)
        return str(filepath)

export_service = ExportService()
