import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = docx.Document()

# Configure Margins (0.8 inch)
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

PRIMARY_COLOR = RGBColor(30, 58, 138)    # Deep Blue
SECONDARY_COLOR = RGBColor(79, 70, 229)  # Indigo
TEXT_COLOR = RGBColor(30, 41, 59)        # Slate Dark
MUTED_COLOR = RGBColor(100, 116, 139)    # Slate Muted

def add_header_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = PRIMARY_COLOR
    p.paragraph_format.space_after = Pt(4)

def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(13)
    run.font.color.rgb = SECONDARY_COLOR
    run.font.italic = True
    p.paragraph_format.space_after = Pt(18)

def add_heading_1(text):
    h = doc.add_paragraph()
    run = h.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = PRIMARY_COLOR
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)

def add_heading_2(text):
    h = doc.add_paragraph()
    run = h.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(12.5)
    run.font.bold = True
    run.font.color.rgb = SECONDARY_COLOR
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(4)

def add_body(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(10.5)
    run.font.color.rgb = TEXT_COLOR
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(5)
    return p

def add_bullet(bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    r1 = p.add_run(bold_prefix)
    r1.font.name = 'Calibri'
    r1.font.size = Pt(10.5)
    r1.font.bold = True
    r1.font.color.rgb = TEXT_COLOR
    r2 = p.add_run(text)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = TEXT_COLOR
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)

def add_screenshot(img_path, caption_text):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(3)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.2))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        run_cap = p_cap.add_run(f"Figure: {caption_text}")
        run_cap.font.name = 'Calibri'
        run_cap.font.size = Pt(9.5)
        run_cap.font.italic = True
        run_cap.font.color.rgb = MUTED_COLOR

# ----------------- DOCUMENT CONTENT -----------------

add_header_title("ClauseAugment AI: Legal Text Data Augmenter & Universal ML Robustness Platform")
add_subtitle("Complete Project Technical Report & Comprehensive Implementation Guide")

add_heading_1("Project Description:")
add_body(
    "ClauseAugment AI is an end-to-end Machine Learning, Natural Language Processing (NLP), and Data Augmentation "
    "platform designed to solve data scarcity, severe class imbalance, and poor generalization in supervised classification "
    "and regression models. In specialized domains such as legal contract analysis, healthcare, and finance, obtaining "
    "large, high-quality, expert-labeled datasets is cost-prohibitive. Machine learning models trained on small datasets "
    "routinely overfit to specific phrasing, rigid templates, or corporate drafting styles, failing when exposed to real-world out-of-distribution variations."
)
add_body(
    "ClauseAugment AI addresses these foundational challenges by offering a controlled data augmentation pipeline. "
    "The system combines traditional algorithmic NLP techniques (WordNet Synonym Replacement, Syntactic Clause Inversion, "
    "Random Swap, Deletion, and Insertion) with optional Google Gemini 2.5 Flash context-aware paraphrasing, and tabular "
    "techniques including SMOTE and Gaussian perturbation. Crucially, every generated variant is subjected to rigorous "
    "semantic cosine validation, negation preservation, and entity retention checks before entering a zero-data-leakage "
    "machine learning evaluation engine."
)

add_heading_2("Real-World Scenarios:")
add_bullet("Scenario 1 (LegalTech Contract Classification): ", 
           "A legal researcher uploads a dataset of 200 contract clauses across 10 categories (e.g., Confidentiality, Indemnification, Force Majeure). "
           "The platform profiles class distributions, generates 1,000 semantically consistent variations without altering legal obligations, "
           "and trains a RandomForest classifier, improving minority class F1-scores by up to +25.0%.")

add_bullet("Scenario 2 (Customer Review Sentiment Analysis): ", 
           "An e-commerce business analyst uploads imbalanced customer review ratings. The system applies Google Gemini context-aware "
           "paraphrasing to expand minority negative reviews, ensuring the sentiment polarity and key adjectives remain intact while introducing lexical diversity.")

add_bullet("Scenario 3 (Financial Risk Assessment): ", 
           "A financial data scientist uploads tabular credit risk records. The platform applies SMOTE and Gaussian noise injection to numerical "
           "columns (e.g., debt-to-income, credit score) while verifying physical boundary constraints (min/max limits), balancing default risk predictions.")

add_heading_1("Technical Architecture:")
add_body(
    "ClauseAugment AI utilizes a decoupled, production-grade three-tier architecture that guarantees zero data leakage "
    "and end-to-end traceability across all data transformations:"
)
add_bullet("Presentation Layer (Frontend): ", "Built with React 18, Vite, and Tailwind CSS. Features an interactive dashboard with Recharts visualizations, Lucide icons, real-time parameter configuration, and SVG confusion matrix displays.")
add_bullet("Application Layer (Backend): ", "Built with FastAPI (Python 3.11+). Orchestrates data profiling, NLP augmentation algorithms, semantic validation pipelines, and scikit-learn model evaluation.")
add_bullet("Persistence Layer (Database): ", "Relational SQLite database powered by SQLAlchemy ORM, managing datasets, original clauses, augmented records, validation results, and training experiment benchmarks.")
add_bullet("AI & Algorithmic Engines: ", "Integrates NLTK WordNet and syntactical clause restructurers for local, deterministic NLP alongside the Google GenAI SDK for Gemini 2.5 Flash context-aware paraphrasing.")

add_heading_2("Database Entity-Relationship (ER) Architecture:")
add_body(
    "The persistence model consists of 6 structured tables ensuring strict referential integrity:\n"
    "• DATASETS: Stores dataset metadata, row counts, and dynamic column mappings.\n"
    "• CLAUSES / DATASET_RECORDS: Stores original input text and categorical ground truth.\n"
    "• AUGMENTED_CLAUSES: Stores synthetic text, generation technique, similarity score, and review status.\n"
    "• VALIDATION_RESULTS: Stores boolean validation flags (cosine threshold, negation match, modal verb check, number retention).\n"
    "• TRAINING_EXPERIMENTS: Records train/test partition sizes, model hyperparameters, and seed configurations.\n"
    "• MODEL_METRICS: Records baseline vs. augmented accuracy, precision, recall, macro F1, and confusion matrices."
)

add_heading_1("Pre-requisites:")
add_bullet("Python Environment: ", "Python 3.10+ (tested on Python 3.11 and 3.14).")
add_bullet("Node.js Runtime: ", "Node.js v18.0+ and npm for frontend compilation.")
add_bullet("FastAPI & Uvicorn: ", "High-performance ASGI server for backend API execution.")
add_bullet("Machine Learning Libraries: ", "Scikit-learn, Pandas, NumPy, and Imbalanced-learn (SMOTE).")
add_bullet("NLP Corpora: ", "NLTK data (WordNet, OMW-1.4, Punkt tokenizers).")
add_bullet("Google GenAI SDK (Optional): ", "google-genai package for optional Gemini 2.5 Flash paraphrasing.")
add_bullet("Version Control & Deployment: ", "Git, GitHub, and Ngrok for public tunneling.")

# ----------------- WORKFLOW & MILESTONES -----------------

add_heading_1("Project Workflow & Milestones:")

add_heading_2("Milestone 1: Model Selection and Architecture")
add_body(
    "Activity 1.1: Configured backend environment variables (.env) supporting optional GEMINI_API_KEY with automatic local fallback.\n"
    "Activity 1.2: Selected Scikit-learn (RandomForest, LinearSVC, LogisticRegression, MultinomialNB) for traditional explainable ML.\n"
    "Activity 1.3: Defined modular directory structure separating API routes, domain services, ML pipelines, and core database models.\n"
    "Activity 1.4: Set up local virtual environment and verified dependencies across Python and npm."
)

add_heading_2("Milestone 2: Core Functionalities Development")
add_body(
    "Activity 2.1: Implemented 6 distinct data augmentation algorithms:\n"
    "  1. WordNet Synonym Replacement: Replaces non-critical tokens while protecting legal terms, modals (shall, must), and negations.\n"
    "  2. Syntactic Sentence Restructuring: Inverts dependent and conditional clauses (e.g., 'If X then Y' -> 'Y if X').\n"
    "  3. Random Word Swap, Deletion, and Insertion: Injects calibrated lexical perturbations to reduce positional overfitting.\n"
    "  4. Google Gemini 2.5 Flash: Context-aware paraphrasing generating fluid semantic alternatives.\n"
    "  5. Tabular SMOTE & Gaussian Jitter: Synthesizes minority feature representations for continuous variables.\n"
    "Activity 2.2: Built multi-tier validation engine enforcing cosine similarity boundaries [0.60, 0.98], negation polarity matching, and numeric token consistency."
)

add_heading_2("Milestone 3: FastAPI Backend & Services Development")
add_body(
    "Activity 3.1: Implemented REST API routes across /datasets, /augmentation, /validation, /training, /evaluation, /robustness, and /export.\n"
    "Activity 3.2: Developed Zero-Data-Leakage training pipeline: data is split into 80% train / 20% test before augmentation; vectorizers fit solely on train; both baseline and augmented models are tested on the exact same held-out test split."
)

add_heading_2("Milestone 4: Frontend Development")
add_body(
    "Activity 4.1: Built React 18 single-page application with Tailwind CSS and responsive sidebar navigation.\n"
    "Activity 4.2: Developed 11 interactive views: Overview Dashboard, Dataset Management, Text Preprocessing, Augmentation Studio, Semantic Validation, Dataset Comparison, Model Training, Evaluation Results, Robustness Testing, Export Center, and Project Documentation."
)

add_heading_2("Milestone 5: Deployment & Public Exposure")
add_body(
    "Activity 5.1: Local production deployment with Uvicorn on port 8000 and Vite on port 5173.\n"
    "Activity 5.2: Public tunneling support using Ngrok for remote demonstrations and live portfolio access."
)

# ----------------- SCREENSHOT ATTACHMENTS -----------------

add_heading_1("Exploring the Website's Web Pages & Empirical Results:")

SCREENSHOT_DIR = r"c:\Users\HP\OneDrive\Desktop\Gen AI\docs\screenshots"

img_eval_overview = os.path.join(SCREENSHOT_DIR, "media_1795571804726_8bc21572.png")
img_class_breakdown = os.path.join(SCREENSHOT_DIR, "media_1795571797908_fd0f0cb1.png")
img_robustness = os.path.join(SCREENSHOT_DIR, "media_1795571794067_7a7cc370.png")
img_dataset_mgmt = os.path.join(SCREENSHOT_DIR, "media_1795570384970_29d0331c.png")
img_overview = os.path.join(SCREENSHOT_DIR, "media_1795570398441_06313825.png")

add_heading_2("1. Evaluation Results & Comparative Metric Gauges:")
add_body(
    "Description: The Evaluation Results screen provides an empirical side-by-side comparison between the Baseline model "
    "(trained strictly on original data) and the Augmented model (trained on original + validated augmented samples), "
    "both evaluated on the exact same unseen held-out test split (40 test clauses). "
    "As shown below, RandomForest achieved a +5.0% Test Accuracy Delta and a +0.0296 Macro F1 Gain (+4.27% relative gain), "
    "confirming robust generalization."
)
add_screenshot(img_eval_overview, "Evaluation Results Dashboard - Comparative Metrics on Held-Out Test Set")

add_heading_2("2. Class-Wise Precision, Recall, and F1 Breakdown:")
add_body(
    "Description: This granular evaluation table proves that data augmentation directly addressed minority class representation. "
    "Indemnification F1 jumped from 0.750 to 1.000 (+0.250 gain), Governing Law improved from 0.727 to 0.889 (+0.162 gain), "
    "and Force Majeure rose from 0.857 to 1.000 (+0.143 gain). Because real-world datasets exhibit slight trade-offs in other classes, "
    "these authentic metrics confirm the validity of our scientific scikit-learn evaluation pipeline."
)
add_screenshot(img_class_breakdown, "Class-Wise Precision, Recall, and F1 Performance Breakdown Across 10 Legal Categories")

add_heading_2("3. Out-of-Distribution Robustness Stress Testing:")
add_body(
    "Description: The Robustness Testing module subjects the trained models to 4 simulated real-world noise perturbations: "
    "Drafting Style Shift, Paraphrase Stress Test, Scanned/OCR Spacing Noise, and Transcription/Casing Permutations. "
    "The results demonstrate positive Resilience Shifts across all perturbation types (+0.0692 on paraphrase stress, +0.0296 on casing), "
    "demonstrating that data augmentation shields the classifier against drafting noise."
)
add_screenshot(img_robustness, "Out-of-Distribution Robustness Stress Testing Across Controlled Perturbations")

add_heading_2("4. Dataset Management & Ingestion Portal:")
add_body(
    "Description: The Dataset Management module allows researchers to upload custom CSV or JSON datasets with automatic schema "
    "validation (clause_id, clause_text, clause_type). It features real-time search, category filtering, word count statistics, "
    "and one-click CSV/JSON dataset exports."
)
add_screenshot(img_dataset_mgmt, "Legal Dataset Management Portal with Custom File Ingestion & Exploration")

add_heading_2("5. Overview Dashboard & Architecture Summary:")
add_body(
    "Description: The Overview Dashboard provides a centralized system status, active legal dataset selection, "
    "total benchmark clause counts, generated variations count, and guided pipeline workflow navigation."
)
add_screenshot(img_overview, "Overview Dashboard with System Status and Metric Cards")

# ----------------- CONCLUSION -----------------

add_heading_1("Conclusion & Future Scope:")
add_body(
    "ClauseAugment AI successfully demonstrates how controlled NLP data augmentation, semantic validation, and traditional "
    "machine learning can solve data scarcity and class imbalance without relying on expensive, black-box paid APIs. "
    "By enforcing a strict zero-data-leakage evaluation protocol, the platform provides verifiable proof of generalization gains, "
    "delivering up to +25.0% F1-score improvements on critical minority legal clauses."
)
add_body(
    "Future roadmap enhancements include:\n"
    "• Offline Transformer Embeddings: Integrating local Sentence-BERT (e.g., all-MiniLM-L6-v2) for air-gapped neural similarity scoring.\n"
    "• Generative Tabular Networks (CTGAN): Adding conditional GAN architectures for complex financial and clinical tabular generation.\n"
    "• Active Learning Feedback Loops: Incorporating interactive human-in-the-loop review interfaces for ambiguous edge cases.\n"
    "• Enterprise Connectors: Adding native PostgreSQL and Snowflake database ingestion pipelines."
)

output_path = r"c:\Users\HP\OneDrive\Desktop\Gen AI\ClauseAugment_AI_Project_Report.docx"
doc.save(output_path)
print(f"Successfully generated DOCX report at: {output_path}")
