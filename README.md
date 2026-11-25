# ClauseAugment AI – Universal Data Augmentation & ML Robustness Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg?style=flat&logo=react)](https://reactjs.org)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python)](https://python.org)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF.svg?style=flat&logo=vite)](https://vitejs.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

ClauseAugment AI is an enterprise-grade universal data augmentation platform designed to systematically evaluate and enhance machine learning robustness across **unstructured text** (legal contracts, e-commerce reviews, clinical notes) and **structured tabular** datasets (credit risk classification, real estate price regression).

---

## 🌟 Key Features

- **Universal Modality & Format Support**: Ingests CSV, JSON, JSONL, and Excel XLSX files. No hardcoded column names; users configure input, target, identifier, and preserved columns interactively.
- **Dynamic Dataset Profiling**: In-depth inspection computing data dimensions, column types, missingness, duplicate rows, and class imbalance ratios.
- **Multi-Algorithm Augmentation Engine**:
  - *Text*: WordNet Synonym Replacement, Sentence Restructuring, Random Insertion, Deletion, Word Swap, and **Google Gemini 2.5 Flash** context-aware paraphrasing.
  - *Tabular*: SMOTE (via `imbalanced-learn`), Random Oversampling with Jitter, Gaussian Noise Injection, Numerical Perturbation ($\pm 8\%$), and Categorical Resampling.
- **Strict Validation Rules**: Multi-tier checks enforcing semantic cosine similarity bounds $[0.60, 0.98]$, negation polarity retention, modal verb preservation, and tabular physical boundary compliance.
- **Zero-Data-Leakage ML Pipeline**: Splits original data into training and held-out test sets *before* augmentation, ensuring preprocessors and augmented models are evaluated solely against untouched test distributions.
- **Interactive UI**: Full-featured React/Vite web application with Recharts visualizations, dark/light themes, and export center (CSV, JSONL, and academic PDF/JSON reports).

---

## 🚀 Quick Start

### 1. Backend Setup
```bash
# Clone the repository
git clone https://github.com/banavathuramkumar/clause-augment-ai.git
cd clause-augment-ai

# Install Python requirements
pip install -r backend/requirements.txt

# Start backend server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 📚 Milestone Documentation
Detailed architectural and methodology documentation is available in the [`docs/`](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs) directory:
1. [Milestone 01: Project Description](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/01_Project_Description.md)
2. [Milestone 02: Problem Statement](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/02_Problem_Statement.md)
3. [Milestone 03: Use Cases & Scenarios](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/03_Use_Cases_and_Scenarios.md)
4. [Milestone 04: Technology Selection](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/04_Technology_Selection.md)
5. [Milestone 05: Technical Architecture](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/05_Technical_Architecture.md)
6. [Milestone 06: Pre-Requisites & Setup](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/06_Pre_Requisites.md)
7. [Milestone 07: Project Workflow](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/07_Project_Workflow.md)
8. [Milestone 08: Milestone 1 Architecture](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/08_Milestone_1_Architecture.md)
9. [Milestone 09: Milestone 2 Ingestion & Preprocessing](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/09_Milestone_2_Dataset_Preprocessing.md)
10. [Milestone 10: Milestone 3 Augmentation & Gemini](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/10_Milestone_3_Augmentation_Gemini.md)
11. [Milestone 11: Milestone 4 Validation Engine](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/11_Milestone_4_Validation.md)
12. [Milestone 12: Milestone 5 ML Pipeline](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/12_Milestone_5_Machine_Learning.md)
13. [Milestone 13: Milestone 6 Frontend Integration](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/13_Milestone_6_Frontend_Integration.md)
14. [Milestone 14: Milestone 6 Testing & Verification](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/14_Milestone_6_Testing.md)
15. [Milestone 15: Deployment Guide & Ngrok](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/15_Deployment_Guide.md)
16. [Milestone 16: Database Schema & ER Diagram](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/16_Database_ER_Diagram.md)
17. [Milestone 17: Test Cases & Empirical Results](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/17_Test_Cases_and_Results.md)
18. [Milestone 18: Conclusion & Future Enhancements](file:///c:/Users/HP/OneDrive/Desktop/Gen%20AI/docs/18_Conclusion_and_Future_Enhancements.md)
