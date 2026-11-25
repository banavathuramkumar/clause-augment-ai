# Milestone 09: Milestone 2 - Universal Dataset Ingestion & Preprocessing

## 1. Universal Ingestion & Auto-Profiling
The platform automatically parses uploaded CSV, JSON, JSONL, and Excel files. During ingestion, the dataset service calculates:
- Dimensions (row count, column count).
- Data type distribution (integer, float, categorical, free-form text, datetime, identifier).
- Missing value counts and ratios per column.
- Duplicate record count.
- Candidate role detection:
  - Text columns with high lexical diversity are flagged as candidate input columns.
  - Columns with discrete categorical labels or continuous values are flagged as candidate targets.
  - Monotonically increasing or UUID-like columns are flagged as candidate identifiers.

---

## 2. Universal Preprocessing Engine
- **Text Cleaning**:
  - Lowercasing and whitespace normalisation.
  - Punctuation stripping with domain exception lists.
  - Stopword filtering using NLTK English stopword lexicon while safeguarding legal/technical terms.
  - Lemmatization via WordNet.
- **Tabular Preprocessing**:
  - Missing value imputation: Mean, Median, Mode, or Drop strategies.
  - Duplicate record deduplication.
  - ColumnTransformer pipelines for numerical feature scaling (StandardScaler) and categorical encoding (OneHotEncoder).
