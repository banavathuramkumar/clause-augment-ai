# ClauseAugment AI – Contract Clause Text Augmenter & ML Robustness Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg?style=flat&logo=react)](https://reactjs.org)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python)](https://python.org)
[![Vite](https://img.shields.io/badge/Vite-6.0+-646CFF.svg?style=flat&logo=vite)](https://vitejs.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0+-38B2AC.svg?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**ClauseAugment AI** is a production-quality, end-to-end Machine Learning and Natural Language Processing (NLP) system designed to solve **data scarcity**, **class imbalance**, and **poor generalization** in contract clause classification.

Contract clause classification models trained on limited legal datasets often fail to generalize across different drafting styles, sentence structures, and contract templates. ClauseAugment AI provides a controlled, explainable, and reproducible legal text data augmentation pipeline that generates diverse but semantically consistent variations of contract clauses while enforcing zero data leakage during evaluation.

---

## 🚀 Key Highlights & Capabilities

- **Zero-Data-Leakage ML Pipeline**:
  - The dataset is strictly partitioned into **80% Train** and **20% Test** splits *before* any data augmentation takes place.
  - Feature extraction pipelines (TF-IDF vectorizers) are fitted *exclusively* on the original training split.
  - Both the **Baseline Model** and the **Augmented Model** are evaluated on the exact same unseen held-out test distribution.
- **Controlled NLP Augmentation Engine**:
  - **WordNet Synonym Replacement**: Replaces non-critical tokens while strictly safeguarding legal terminology, modals (`shall`, `must`), and negations (`not`, `never`).
  - **Syntactic Sentence Restructuring**: Inverts dependent and conditional clauses (e.g., *"If X occurs, Provider shall Y"* $\to$ *"Provider shall Y if X occurs"*).
  - **Random Insertion, Deletion, and Swap**: Injects controlled lexical noise to reduce positional overfitting.
  - **Optional Google Gemini 2.5 Flash**: Context-aware paraphrasing via the `google-genai` SDK with automatic, zero-dependency offline fallback.
- **Multi-Tier Semantic & Legal Validation**:
  - **Cosine Similarity Bound**: Enforces TF-IDF cosine similarity within $[0.60, 0.98]$ to prevent topic drift or identical copies.
  - **Negation Polarity Retention**: Immediately flags `NEGATION_MISMATCH` if negative words are flipped.
  - **Obligation Modals & Number Retention**: Ensures critical duty verbs and numerical entities/dates remain intact.
- **Out-of-Distribution Robustness Stress Testing**:
  - Simulates 4 real-world noise perturbations: *Drafting Style Shifts*, *Paraphrase Stress*, *OCR Spacing Noise*, and *Transcription Typographical Permutations*.
- **Interactive Full-Stack Web Application**:
  - Built with **React 18**, **Vite**, **Tailwind CSS**, and **Recharts**.
  - Dynamic dataset uploader (CSV / JSON), real-time clause explorer, parameter sliders, and side-by-side performance comparison charts.

---

## 🏛️ System Architecture

```
ClauseAugment AI
├── Frontend (React 18 + Vite + Tailwind CSS + Recharts)
│   ├── Overview Dashboard (Benchmark metrics & system status)
│   ├── Dataset Management (CSV/JSON upload & clause explorer)
│   ├── Text Preprocessing (Interactive NLP sandbox)
│   ├── Augmentation Studio (Multi-algorithm configuration & preview)
│   ├── Semantic Validation (Integrity flags & similarity scores)
│   ├── Model Training (Zero-leakage training launcher)
│   ├── Evaluation Results (Comparative accuracy, F1 delta, confusion matrix)
│   ├── Robustness Testing (Perturbation resilience shifts)
│   └── Export Center (CSV & JSON dataset downloads)
│
├── Backend (FastAPI + Pydantic + SQLAlchemy ORM)
│   ├── REST API Routes (/datasets, /augmentation, /validation, /training, /evaluation, /robustness, /export)
│   ├── Algorithms (Synonym replacement, restructuring, deletion, insertion, swap, Gemini)
│   ├── Services (Dataset, preprocessing, augmentation, validation, training, robustness)
│   └── ML Core (Feature extraction, classifiers, metrics, zero-leakage experiment runner)
│
└── Database (SQLite: clause_augment.db)
    ├── datasets (Metadata, clause counts, categories)
    ├── clauses (Original benchmark & user-uploaded clauses)
    ├── augmented_clauses (Synthetic text variations & techniques)
    ├── validation_results (Cosine scores, flags, review status)
    ├── training_experiments (Train/test sizes, seeds, model configs)
    └── model_metrics (Accuracy, precision, recall, macro F1, confusion matrices)
```

---

## 📊 Supported Legal Categories

The system includes a pre-seeded benchmark dataset covering **200 contract clauses across 10 core legal categories**:
1. **Confidentiality**
2. **Indemnification**
3. **Termination**
4. **Liability**
5. **Governing Law**
6. **Payment**
7. **Force Majeure**
8. **Dispute Resolution**
9. **Intellectual Property**
10. **Data Protection**

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.11+, FastAPI, Pydantic, SQLAlchemy, Uvicorn |
| **Machine Learning** | Scikit-learn (RandomForest, LinearSVC, LogisticRegression, MultinomialNB), Imbalanced-learn |
| **NLP** | NLTK (WordNet, Punkt Tokenizers, Stopwords) |
| **Generative AI** | Google GenAI SDK (`gemini-2.5-flash`, optional with offline fallback) |
| **Frontend** | React 18, Vite, Tailwind CSS, Recharts, Lucide Icons |
| **Database** | SQLite, SQLAlchemy ORM |
| **Testing** | Pytest, HTTPX |

---

## ⚡ Quick Start & Installation

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.11 and 3.14)
- Node.js v18+ and npm
- Git

### 2. Clone Repository
```bash
git clone https://github.com/banavathuramkumar/clause-augment-ai.git
cd clause-augment-ai
```

### 3. Backend Setup
```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# (Optional) Set up Google Gemini API key
# Copy .env.example to .env and add your key:
# GEMINI_API_KEY=your_gemini_api_key_here
# GEMINI_MODEL_NAME=gemini-2.5-flash

# Start the FastAPI backend server
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
The backend API and interactive Swagger documentation will be available at:
- **API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4. Frontend Setup
Open a second terminal window:
```bash
cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```
Open your browser and navigate to:
- **Web Application**: [http://localhost:5173](http://localhost:5173)

---

## 📂 Detailed File Structure

```
clause-augment-ai/
│
├── backend/                                # FastAPI Python backend application
│   ├── app/
│   │   ├── main.py                         # Application entry point, lifespan, CORS, route inclusion
│   │   ├── config.py                       # Global settings, paths, thresholds, preserved legal keywords
│   │   │
│   │   ├── api/routes/                     # REST API endpoints
│   │   │   ├── dataset.py                  # Dataset ingestion, clause browsing, expansion summaries
│   │   │   ├── preprocessing.py            # Text cleaning, stopword removal, lemmatization
│   │   │   ├── augmentation.py             # Generating variations, approvals, and rejections
│   │   │   ├── validation.py               # Semantic validation scores, flags, and review status
│   │   │   ├── training.py                 # ML model training launcher and experiment management
│   │   │   ├── evaluation.py               # Model metrics, classification reports, confusion matrices
│   │   │   ├── robustness.py               # Out-of-distribution stress testing and perturbation analysis
│   │   │   └── export.py                   # Data export endpoints (CSV, JSON, PDF reports)
│   │   │
│   │   ├── core/                           # Database & validation models
│   │   │   ├── database.py                 # SQLAlchemy engine, session maker, base declarative model
│   │   │   ├── models.py                   # Database entities (Dataset, Clause, AugmentedClause, Experiment)
│   │   │   └── schemas.py                  # Pydantic schemas for request/response serialization
│   │   │
│   │   ├── services/                       # Business logic service layer
│   │   │   ├── dataset_service.py          # Benchmark dataset loading, stats calculation, parsing
│   │   │   ├── preprocessing_service.py    # NLTK-based text cleaning and tokenization
│   │   │   ├── augmentation_service.py     # Augmentation pipeline orchestration
│   │   │   ├── validation_service.py       # Cosine similarity and legal constraint verification
│   │   │   ├── training_service.py         # Model training execution, artifact persistence, evaluation
│   │   │   ├── robustness_service.py       # Perturbation injection and model resilience scoring
│   │   │   └── export_service.py           # Report formatting and export delivery
│   │   │
│   │   ├── ml/                             # Traditional Machine Learning core
│   │   │   ├── feature_extraction.py       # TF-IDF unigram & bigram vectorizer pipelines
│   │   │   ├── classifiers.py              # Model factory (RandomForest, LinearSVC, LogisticRegression, MNB)
│   │   │   ├── metrics.py                  # Accuracy, Macro/Weighted F1, Precision, Recall, Confusion Matrix
│   │   │   └── experiment.py               # Strict Zero-Data-Leakage train/test split experiment runner
│   │   │
│   │   ├── algorithms/                     # Data augmentation algorithmic transformers
│   │   │   ├── base.py                     # Base augmenter abstract class & legal word protection rules
│   │   │   ├── synonym_replacement.py      # WordNet-based synonym substitution
│   │   │   ├── sentence_restructuring.py   # Syntactic clause inversion and clause transposition
│   │   │   ├── random_insertion.py         # Contextual random synonym insertion
│   │   │   ├── random_deletion.py          # Controlled non-critical token deletion
│   │   │   ├── random_swap.py              # Random word order transposition
│   │   │   ├── back_translation.py         # Paraphrase translation transformer
│   │   │   └── gemini_augmenter.py         # Google Gemini 2.5 Flash context-aware paraphrasing
│   │   │
│   │   └── utils/                          # Utility helpers
│   │       ├── text_cleaner.py             # Regex cleaning and token preservation helpers
│   │       ├── file_handler.py             # File saving, reading, and directory helpers
│   │       └── logger.py                   # Centralized application logging
│   │
│   ├── datasets/                           # Benchmark datasets storage
│   │   └── sample_contract_clauses.csv     # 200 contract clauses across 10 legal categories
│   ├── trained_models/                     # Serialized scikit-learn models (.joblib)
│   ├── exports/                            # Exported CSV, JSON, and PDF evaluation reports
│   ├── tests/                              # Automated test suite
│   │   └── test_clause_augment.py          # Pytest integration and algorithmic test cases
│   ├── clause_augment.db                   # SQLite database
│   └── requirements.txt                    # Python dependencies
│
├── frontend/                               # React + Vite frontend application
│   ├── src/
│   │   ├── components/                     # Reusable UI components
│   │   │   ├── Header.jsx                  # Top navigation bar, dataset selector, sync status
│   │   │   ├── Sidebar.jsx                 # Collapsible navigation drawer
│   │   │   └── StatCard.jsx                # Metrics card display component
│   │   │
│   │   ├── pages/                          # Application views and dashboard modules
│   │   │   ├── Overview.jsx                # Benchmark summary, metric cards, pipeline workflow
│   │   │   ├── DatasetManagement.jsx       # CSV/JSON file uploader, clause explorer, search/filter
│   │   │   ├── TextPreprocessing.jsx       # Interactive NLP cleaning sandbox and token inspection
│   │   │   ├── AugmentationStudio.jsx      # Multi-technique generation interface and live previews
│   │   │   ├── SemanticValidation.jsx      # Cosine score inspection, flag reasons, approval actions
│   │   │   ├── DatasetComparison.jsx       # Category distribution comparison before & after augmentation
│   │   │   ├── ModelTraining.jsx           # Zero-leakage experiment launcher and hyperparameter selection
│   │   │   ├── EvaluationResults.jsx       # Side-by-side metric charts, confusion matrices, F1 deltas
│   │   │   ├── RobustnessTesting.jsx       # Stress-testing perturbations and resilience gauges
│   │   │   ├── ExportCenter.jsx            # One-click dataset and evaluation report downloads
│   │   │   └── ProjectDocs.jsx             # In-app architecture reference and technical guide
│   │   │
│   │   ├── services/
│   │   │   └── api.js                      # Centralized API service interacting with FastAPI backend
│   │   ├── App.jsx                         # Main layout, tab navigation, and shared application state
│   │   ├── index.css                       # Tailwind CSS directives and custom styling
│   │   └── main.jsx                        # React root component initialization
│   │
│   ├── package.json                        # Frontend packages and build scripts
│   ├── tailwind.config.js                  # Tailwind design system configuration
│   └── vite.config.js                      # Vite build configuration and API reverse proxy
│
├── .env.example                            # Environment variables template
├── .gitignore                              # Git exclusion rules
└── README.md                               # Comprehensive project documentation
```

---

## 🧪 Testing

Execute the automated test suite covering unit algorithms, API routes, and zero-leakage validation:
```bash
pytest backend/tests/test_clause_augment.py -v
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
