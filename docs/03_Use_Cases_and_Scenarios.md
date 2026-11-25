# Milestone 03: Use Cases and Scenarios

## 1. Domain Scenarios & Workflows

### Scenario A: Legal Contract Analysis (Unstructured Text Classification)
- **User**: Corporate Legal Counsel / LegalTech ML Researcher.
- **Data**: Contract clauses across 10 categories (Confidentiality, Indemnification, Governing Law, Force Majeure).
- **Challenge**: Templates from different law firms vary in phrasing; minority clauses (e.g., Force Majeure) have few samples.
- **Pipeline**: Ingest CSV $\to$ Profile `clause_text` and `clause_type` $\to$ Apply Synonym Replacement and Sentence Restructuring $\to$ Cosine & Negation Validation $\to$ Train LinearSVC classifier.
- **Outcome**: Improved Macro F1 on minority clauses without semantic shift.

### Scenario B: E-Commerce Customer Reviews (Sentiment Classification)
- **User**: Retail Product Analyst.
- **Data**: Customer reviews (`review_text`, `sentiment`, `product_category`).
- **Pipeline**: Ingest $\to$ Apply Google Gemini Context-Aware Paraphrasing and EDA $\to$ Validate label preservation $\to$ Train Logistic Regression baseline vs. augmented.

### Scenario C: Financial Credit Risk (Tabular Classification)
- **User**: Financial Risk Scientist.
- **Data**: Credit applicant features (`age`, `annual_income`, `credit_score`, `loan_amount`, `debt_to_income`, `default_risk`).
- **Challenge**: Severe default class imbalance ($> 4:1$).
- **Pipeline**: Ingest $\to$ Apply SMOTE and Gaussian Jitter $\to$ Validate physical range bounds $\to$ Train Random Forest Classifier.

### Scenario D: Real Estate House Price Prediction (Tabular Regression)
- **User**: Econometrician / Real Estate Data Scientist.
- **Data**: Property attributes (`square_feet`, `bedrooms`, `bathrooms`, `location_zone`, `price_thousands`).
- **Pipeline**: Ingest $\to$ Apply Bounded Numerical Perturbation ($\pm 8\%$) $\to$ Validate continuous bounds $\to$ Train Ridge Regressor $\to$ Evaluate MAE and $R^2$ reduction.

### Scenario E: Healthcare Clinical Notes (Unlabeled Text Augmentation)
- **User**: Medical Informatics Researcher.
- **Data**: Unlabeled clinical summaries (`note_id`, `clinical_notes`, `department`).
- **Pipeline**: Ingest $\to$ Augment text with Sentence Restructuring and Gemini $\to$ Export expanded dataset without training a classifier.
