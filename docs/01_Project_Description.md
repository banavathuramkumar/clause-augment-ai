# Milestone 01: Project Description

## 1. Executive Summary
**ClauseAugment AI** is a universal data augmentation and machine learning robustness platform designed to address the challenges of data scarcity, class imbalance, and poor model generalization across diverse data domains. Unlike legacy tools that are locked to specific schemas or single domains (such as legal contracts), ClauseAugment AI provides universal dataset processing across **unstructured text** (legal clauses, e-commerce reviews, clinical notes) and **structured tabular** datasets (financial credit risk, real estate regression).

The system integrates algorithmic data augmentation (rule-based NLP transformations, SMOTE, Gaussian noise, and numerical perturbations) alongside optional **Google Gemini LLM context-aware paraphrasing**. Every generated record is validated through a multi-tier semantic and schema integrity engine, followed by zero-data-leakage model evaluation.

---

## 2. Platform Highlights
- **Universal Modality Support**: Ingests and processes text, tabular, and mixed datasets across CSV, JSON, JSONL, and Excel XLSX formats.
- **Dynamic Profiling**: Automatically computes statistical summaries, detects data types, flags missing values, computes class imbalance ratios, and identifies candidate feature and target columns.
- **Zero-Data-Leakage ML Pipeline**: Strictly splits datasets into train and test sets *before* augmentation occurs, transforms data using split-isolated pipelines, and validates both baseline and augmented models against the identical held-out test distribution.
- **Multi-Algorithm Augmentation Engine**:
  - *Text*: Synonym Replacement (WordNet), Sentence Restructuring, Random Word Swap, Random Deletion, Random Insertion, and Google Gemini API context-aware paraphrasing.
  - *Tabular*: SMOTE (Synthetic Minority Over-sampling Technique), Random Oversampling with Gaussian jitter, Gaussian Noise Injection, Numerical Feature Perturbation ($\pm 8\%$), and Categorical Resampling.
- **Strict Validation Architecture**:
  - *Text*: Cosine semantic similarity bound $[0.60, 0.98]$, strict negation polarity retention, modal verb preservation, numerical token consistency, and token drift constraints.
  - *Tabular*: Physical domain span constraints ($\pm 15\%$), categorical domain integrity checks, and data type retention.
