# Milestone 04: Technology Selection

## 1. Architecture & Stack Rationale

| Layer | Technology | Selection Justification |
|---|---|---|
| **Backend Framework** | FastAPI (Python 3.11+) | Async high-performance routing, automatic OpenAPI specification, strict Pydantic type validation. |
| **Data Processing** | Pandas, NumPy | Industry-standard tabular manipulation, statistical profiling, and vectorized array operations. |
| **Traditional ML** | Scikit-learn, Imbalanced-learn | Proven classifiers (LogisticRegression, LinearSVC, RandomForest), regressors (Ridge, LinearRegression), feature extraction (TF-IDF, ColumnTransformer), and SMOTE. |
| **NLP Engine** | NLTK (WordNet, Punkt) | Local algorithmic lexical resources for deterministic, explainable, and zero-cost augmentation. |
| **LLM Integration** | Google GenAI SDK (`google-genai`) | Official modern SDK for Gemini context-aware augmentation with graceful local fallback when keys are absent. |
| **Database** | SQLite + SQLAlchemy ORM | Zero-configuration persistence for datasets, column metadata, augmented records, and experiment metrics. |
| **Frontend Framework** | React.js 18 + Vite | Lightning-fast HMR, component modularity, modern asset bundling, and clean state handling. |
| **Styling & Icons** | Tailwind CSS + Lucide React | Clean enterprise design system, dark-mode ready, fully responsive UI. |
| **Data Visualization** | Recharts | Interactive SVG charts for confusion matrices, class distribution changes, and metric gain deltas. |
