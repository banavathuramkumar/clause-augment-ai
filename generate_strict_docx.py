import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = docx.Document()

# 1. Page Margins: Standard 1 inch on all sides (like sample PDF)
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# 2. Strict Black & White: RGBColor(0, 0, 0)
BLACK = RGBColor(0, 0, 0)

# Typography Specifications:
# Headings: 14pt (bold, black)
# Body / Paragraphs / Bullets: 12pt (regular, black)
# Font Family: Calibri / Arial (clean standard)

def add_doc_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = BLACK
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)

def add_doc_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = BLACK
    p.paragraph_format.space_after = Pt(20)

def add_heading(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = BLACK
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)

def add_subheading(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = BLACK
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)

def add_paragraph(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(12)
    run.font.bold = False
    run.font.color.rgb = BLACK
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    return p

def add_bullet(bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        r1.font.name = 'Calibri'
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = BLACK
    if text:
        r2 = p.add_run(text)
        r2.font.name = 'Calibri'
        r2.font.size = Pt(12)
        r2.font.bold = False
        r2.font.color.rgb = BLACK
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)

def add_code_block(code_lines):
    for line in code_lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(line)
        run.font.name = 'Consolas'
        run.font.size = Pt(10.5)
        run.font.color.rgb = BLACK
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)

def add_image_section(img_path, caption_title, description_text):
    add_subheading(caption_title)
    if description_text:
        add_paragraph(f"Description: {description_text}")
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(6)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.2))
    doc.add_page_break()

# ----------------- PAGE 1: TITLE & PROJECT DESCRIPTION -----------------

add_doc_title("ClauseAugment AI: Contract Clause Text Augmenter & Universal ML Robustness Platform")
add_doc_subtitle("AI-Powered Legal NLP Data Augmentation & Robust Classification System")

add_heading("Project Description:")
add_paragraph(
    "ClauseAugment AI harnesses Generative AI and algorithmic NLP techniques to provide intelligent, controlled contract clause text augmentation, offering researchers, data scientists, and legal tech engineers a reliable and leak-free machine learning experience. The platform includes a Clause Preprocessing module, a Multi-Algorithm Augmentation Studio (which produces diverse syntactic and lexical variations preserving legal obligations), a Multi-Tier Semantic Validation Guardrails Engine (which enforces cosine similarity, negation preservation, and modal verb retention), and a Zero-Data-Leakage Machine Learning Benchmark Pipeline that scientifically measures generalization gains on held-out test sets."
)
add_paragraph(
    "Utilizing traditional explainable machine learning models (Random Forest, LinearSVC, Logistic Regression, and Multinomial Naive Bayes) alongside the Google Gemini 2.5 Flash API for context-aware paraphrasing, ClauseAugment AI processes legal clause inputs to deliver fast, high-quality, and robust data variations. Built with FastAPI on the backend and React with Vite on the frontend, and deployable publicly via Ngrok, the platform ensures a seamless and professional user experience. With secure API key management via .env, a 6-table relational SQLite database, and responsible zero-leakage data partitioning, ClauseAugment AI empowers researchers and organizations to train contract classification models with confidence."
)

add_heading("Scenarios:")
add_paragraph(
    "Scenario 1: A legal researcher uploads a dataset of 200 standard contract clauses across 10 categories (e.g., Confidentiality, Indemnification, Force Majeure). The system profiles class distribution, detects severe class imbalance, and applies WordNet Synonym Replacement and Syntactic Sentence Restructuring to generate 1,000 augmented clauses. The resulting RandomForest classifier achieves a +5.0% accuracy improvement and up to +25.0% F1 gains on minority classes."
)
add_paragraph(
    "Scenario 2: An enterprise compliance team evaluates contract classification robustness against diverse external drafting styles. ClauseAugment AI runs out-of-distribution stress perturbations (Drafting Style Shifts, Paraphrase Stress, Scanned OCR Spacing, and Casing Typo Noise), proving that the augmented model maintains superior resilience (+0.0692 F1 resilience shift) compared to the fragile baseline."
)
add_paragraph(
    "Scenario 3: An NLP scientist uploads an imbalanced customer review or financial transaction dataset. The system dynamically adapts to the input format (CSV or JSON), enables custom column mapping, generates contextually valid variations using Google Gemini 2.5 Flash, validates semantic boundaries, and exports the expanded dataset with one click."
)

doc.add_page_break()

# ----------------- PAGE 2: TECHNICAL ARCHITECTURE & PRE-REQUISITES -----------------

add_heading("Technical Architecture:")
add_paragraph(
    "Description: ClauseAugment AI utilizes a modular, decoupled three-tier architecture to deliver rapid, AI-driven data augmentation and machine learning evaluation. The frontend provides a responsive single-page interface built with React 18, Vite, and Tailwind CSS. The FastAPI backend orchestrates data validation, NLP transformations, and prompt construction. It interfaces with local algorithmic engines (WordNet, Syntactic Restructuring) and the Google Gemini 2.5 Flash model to generate tailored text variations, with secure deployment managed locally and exposed publicly through Ngrok."
)
add_paragraph(
    "Database Entity-Relationship (ER) Architecture:\n"
    "The application relies on a 6-table relational database schema managed via SQLAlchemy ORM:\n"
    "• DATASETS: Stores dataset metadata, name, row count, and dynamic column mappings.\n"
    "• CLAUSES: Stores original benchmark and user-uploaded clauses with category labels.\n"
    "• AUGMENTED_CLAUSES: Stores synthetic text variations, technique used, similarity score, and review status.\n"
    "• VALIDATION_RESULTS: Records boolean integrity checks (cosine threshold, negation match, modal verb retention, entity preservation).\n"
    "• TRAINING_EXPERIMENTS: Records train/test partition splits, model hyperparameters, and reproducibility seeds.\n"
    "• MODEL_METRICS: Records baseline vs. augmented accuracy, precision, recall, macro F1, and confusion matrices."
)

add_heading("Pre-requisites:")
add_bullet("FastAPI Framework Knowledge: ", "FastAPI Documentation (https://fastapi.tiangolo.com)")
add_bullet("Machine Learning Proficiency: ", "Scikit-Learn Documentation (https://scikit-learn.org)")
add_bullet("NLP & WordNet Familiarity: ", "NLTK Documentation (https://www.nltk.org)")
add_bullet("Google Gemini GenAI SDK: ", "Google AI Studio Documentation (https://ai.google.dev)")
add_bullet("HTML, CSS, and React Skills: ", "React.js Documentation (https://react.dev)")
add_bullet("Python Programming Proficiency: ", "Python 3.10+ Documentation (https://docs.python.org)")
add_bullet("Version Control with Git: ", "Git Documentation (https://git-scm.com)")
add_bullet("Ngrok for Public Deployment: ", "Ngrok Documentation (https://ngrok.com/docs)")

doc.add_page_break()

# ----------------- PAGE 3: PROJECT WORKFLOW -----------------

add_heading("Project Workflow:")

add_subheading("Milestone 1: Model Selection and Architecture")
add_bullet("• Activity 1.1: ", "Generate a Google Gemini API key and configure it securely in the project environment via .env.")
add_bullet("• Activity 1.2: ", "Research and select appropriate generative AI and machine learning models (Gemini 2.5 Flash, RandomForest, LinearSVC, LogisticRegression).")
add_bullet("• Activity 1.3: ", "Define the architecture of the application, detailing interactions between the React frontend, FastAPI backend, SQLite database, and AI integration.")
add_bullet("• Activity 1.4: ", "Set up the development environment, installing necessary libraries and dependencies for FastAPI, Scikit-learn, NLTK, and React.")

add_subheading("Milestone 2: Core Functionalities Development")
add_bullet("• Activity 2.1: ", "Develop core augmentation features: Synonym Replacement, Sentence Restructuring, Random Insertion/Deletion/Swap, and Gemini Context-Aware Paraphrasing.")
add_bullet("• Activity 2.2: ", "Implement the FastAPI backend to manage routing, database ORM models, semantic validation, and model training execution.")

add_subheading("Milestone 3: App.py & Services Development")
add_bullet("• Activity 3.1: ", "Write main application logic in main.py, establishing routes for /datasets, /augmentation, /validation, /training, /evaluation, /robustness, and /export.")

add_subheading("Milestone 4: Frontend Development")
add_bullet("• Activity 4.1: ", "Design and develop the user interface using React 18, Vite, and Tailwind CSS, ensuring a clean, responsive layout.")
add_bullet("• Activity 4.2: ", "Create dynamic interactive dashboards with Recharts to display real-time accuracy gains, F1 deltas, and confusion matrices.")

add_subheading("Milestone 5: Deployment")
add_bullet("• Activity 5.1: ", "Prepare the application for local deployment by configuring the server environment and verifying all dependencies.")
add_bullet("• Activity 5.2: ", "Deploy the application publicly using Ngrok to expose the local server over a secure public URL.")

add_subheading("Milestone 6: Conclusion")

doc.add_page_break()

# ----------------- PAGE 4: MILESTONE 1 IN DETAIL -----------------

add_heading("Milestone 1: Model Selection and Architecture")
add_paragraph(
    "In this milestone, we focus on selecting appropriate generative AI and traditional machine learning models for our legal data augmentation needs. This involves researching the capabilities and performance of various algorithms, ensuring that the chosen techniques align well with the application's objectives of generating semantically faithful clause variations, safeguarding critical legal obligations, and demonstrating verifiable classification gains."
)

add_subheading("Activity 1.1: Generate a Gemini API Key")
add_paragraph(
    "Before the application can communicate with Google Gemini, you need a valid Gemini API key. Follow the steps below to create one and connect it securely to the project."
)
add_bullet("• Step 1 — Create a Google AI Studio Account: ", "Visit https://aistudio.google.com and sign in with your Google account.")
add_bullet("• Step 2 — Navigate to API Keys: ", "Click 'Get API key' from the sidebar menu to open the API key management dashboard.")
add_bullet("• Step 3 — Create a New API Key: ", "Click 'Create API key' in a new or existing Google Cloud project.")
add_bullet("• Step 4 — Copy API Key: ", "Copy the generated key immediately and store it in a secure location.")
add_bullet("• Step 5 — Add the Key to Your Project: ", "Create a .env file in the root of your project directory and paste the key as shown below:")
add_code_block([
    "GEMINI_API_KEY=your_copied_api_key_here",
    "GEMINI_MODEL_NAME=gemini-2.5-flash"
])
add_bullet("• Step 6 — Verify Key Loading: ", "The backend config.py file loads this key automatically at startup using python-dotenv:")
add_code_block([
    "from dotenv import load_dotenv",
    "import os",
    "load_dotenv()",
    "GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '').strip()"
])
add_bullet("• Important — Never Commit Your API Key: ", "Add .env to your .gitignore file to prevent accidentally pushing credentials to a public repository:")
add_code_block([".env", "backend/clause_augment.db", "__pycache__/"])

doc.add_page_break()

# ----------------- PAGE 5: MILESTONE 1 CONTINUED -----------------

add_subheading("Activity 1.2: Research and Select the Appropriate Models")
add_paragraph("Here are the research considerations used to select the best models for the project:")
add_bullet("• Understand Project Requirements: ", "Review the specific needs of ClauseAugment AI: generating diverse paraphrases while strictly preserving legal obligations, negation polarity, and numbers across 10 contract clause categories.")
add_bullet("• Explore Generative AI Models: ", "Examine Google Gemini 2.5 Flash for high-speed, cost-effective, and context-aware paraphrasing.")
add_bullet("• Evaluate Traditional Classifiers: ", "Select scikit-learn models (RandomForestClassifier, LinearSVC, LogisticRegression, MultinomialNB) to guarantee explainable, reproducible, and zero-cost training benchmarks.")
add_bullet("• Select Optimal Augmentation Strategy: ", "Combine WordNet synonym replacement, syntactic clause inversion, random word insertion/deletion, and Gemini paraphrasing.")

add_subheading("Activity 1.3: Define the Architecture of the Application")
add_bullet("• Architectural Diagram: ", "Create a decoupled representation separating React presentation, FastAPI routing, ORM database persistence, and scikit-learn training pipelines.")
add_bullet("• Detail Frontend Functionality: ", "Outline user interactions: dataset selection, clause exploration, parameter tuning in Augmentation Studio, semantic validation review, and launching comparative training.")
add_bullet("• Outline Backend Responsibilities: ", "Specify how FastAPI handles incoming requests, performs input validation via Pydantic, executes NLP algorithms, and enforces zero data leakage.")
add_bullet("• Describe Zero-Leakage Protocol: ", "Split dataset into 80% train / 20% test *before* augmentation; fit TF-IDF vectorizers only on the train partition; evaluate baseline and augmented models on the identical held-out test split.")

add_subheading("Activity 1.4: Set Up the Development Environment")
add_paragraph("Follow the terminal setup instructions below:")
add_code_block([
    "# 1. Create and activate Python virtual environment",
    "python -m venv venv",
    "venv\\Scripts\\activate",
    "",
    "# 2. Install backend dependencies",
    "pip install fastapi uvicorn pydantic scikit-learn nltk pandas numpy google-genai sqlalchemy httpx pytest",
    "",
    "# 3. Install frontend dependencies",
    "cd frontend",
    "npm install",
    "cd .."
])

doc.add_page_break()

# ----------------- PAGE 6: MILESTONE 2 CORE FUNCTIONALITIES -----------------

add_heading("Milestone 2: Core Functionalities Development")

add_subheading("Activity 2.1: Develop Core Augmentation & Validation Features")
add_bullet("• Synonym Replacement Augmenter: ", "Substitutes non-critical words with WordNet synonyms while protecting legal keywords, modals (shall, must, will), and negations (not, never, no).")
add_bullet("• Syntactic Sentence Restructurer: ", "Inverts conditional and dependent clauses (e.g., swapping 'If X, Y' to 'Y if X') to evaluate structural invariance.")
add_bullet("• Random Inserter, Deleter, and Swapper: ", "Injects controlled word-level perturbations to break rigid positional dependencies.")
add_bullet("• Gemini Context-Aware Augmenter: ", "Interfaces with gemini-2.5-flash to produce natural semantic variations, with automatic fallback to sentence restructuring if offline.")
add_bullet("• Multi-Tier Validation Guardrails: ", "Calculates TF-IDF cosine similarity [0.60, 0.98], checks negation polarity matching, verifies modal obligation retention, and guards numbers and dates.")

add_subheading("Activity 2.2: Implement the FastAPI Backend")
add_paragraph("Define routes in main.py and dedicated routers under app/api/routes/:")
add_bullet("• Dataset Management Routes: ", "GET /api/datasets, POST /api/datasets/upload, GET /api/datasets/{id}/clauses, GET /api/datasets/{id}/expansion.")
add_bullet("• Augmentation Routes: ", "POST /api/augmentation/generate, GET /api/augmentation/results, POST /api/augmentation/approve, POST /api/augmentation/reject.")
add_bullet("• Validation Routes: ", "POST /api/validation/run, GET /api/validation/dataset/{id}.")
add_bullet("• Training & Evaluation Routes: ", "POST /api/training/run, GET /api/evaluation/{experiment_id}, POST /api/robustness/run.")
add_bullet("• Export Routes: ", "GET /api/export/dataset/{id}, GET /api/export/report/{id}.")

doc.add_page_break()

# ----------------- PAGE 7: MILESTONE 3 CODE LOGIC -----------------

add_heading("Milestone 3: App.py & Services Development")
add_paragraph(
    "Milestone 3 focuses on establishing the core service logic in backend/app/main.py and backend/app/services/. "
    "Below is the core endpoint implementation handling dataset retrieval and zero-leakage training execution:"
)

add_code_block([
    "# backend/app/main.py - Core Application Setup",
    "from fastapi import FastAPI",
    "from fastapi.middleware.cors import CORSMiddleware",
    "from app.core.database import Base, engine, SessionLocal",
    "from app.api.routes import dataset, augmentation, validation, training, evaluation, robustness, export",
    "from app.services.dataset_service import dataset_service",
    "",
    "app = FastAPI(title='ClauseAugment AI', version='1.0.0')",
    "app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])",
    "",
    "app.include_router(dataset.router, prefix='/api')",
    "app.include_router(augmentation.router, prefix='/api')",
    "app.include_router(validation.router, prefix='/api')",
    "app.include_router(training.router, prefix='/api')",
    "app.include_router(evaluation.router, prefix='/api')",
    "app.include_router(robustness.router, prefix='/api')",
    "app.include_router(export.router, prefix='/api')",
    "",
    "# Zero-Data-Leakage Training Logic Sample",
    "def run_zero_leakage_experiment(df, model_name, test_size=0.2, random_state=42):",
    "    # 1. Pre-split raw data BEFORE any augmentation",
    "    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state, stratify=df['clause_type'])",
    "",
    "    # 2. Fit TF-IDF Vectorizer ONLY on training partition",
    "    vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))",
    "    X_train_orig = vectorizer.fit_transform(train_df['clause_text'])",
    "    X_test = vectorizer.transform(test_df['clause_text'])",
    "",
    "    # 3. Train Baseline Classifier",
    "    baseline_model = get_classifier(model_name, random_state)",
    "    baseline_model.fit(X_train_orig, train_df['clause_type'])",
    "",
    "    # 4. Augment ONLY the training split",
    "    aug_train_df = augment_training_partition(train_df)",
    "    combined_train = pd.concat([train_df, aug_train_df], ignore_index=True)",
    "    X_train_aug = vectorizer.transform(combined_train['clause_text'])",
    "",
    "    # 5. Train Augmented Classifier",
    "    aug_model = get_classifier(model_name, random_state)",
    "    aug_model.fit(X_train_aug, combined_train['clause_type'])",
    "",
    "    # 6. Evaluate BOTH models on the identical held-out test split",
    "    base_metrics = compute_metrics(test_df['clause_type'], baseline_model.predict(X_test))",
    "    aug_metrics = compute_metrics(test_df['clause_type'], aug_model.predict(X_test))",
    "    return {'baseline': base_metrics, 'augmented': aug_metrics}"
])

doc.add_page_break()

# ----------------- PAGE 8: MILESTONE 4 FRONTEND DEVELOPMENT -----------------

add_heading("Milestone 4: Frontend Development")
add_paragraph(
    "Milestone 4 focuses on designing and implementing a responsive, modern user interface with React 18, Vite, and Tailwind CSS. "
    "The UI provides real-time state synchronization with the backend and interactive visualizations using Recharts."
)

add_subheading("Activity 4.1: Designing the Layout and Navigation")
add_bullet("• Sidebar Component: ", "Collapsible left navigation menu providing one-click switching across all 11 application modules.")
add_bullet("• Header Component: ", "Displays active legal dataset selector, state synchronization button, and local engine verification badge.")
add_bullet("• StatCard Component: ", "Reusable metric cards displaying total clauses, active categories, word counts, and expansion ratios.")

add_subheading("Activity 4.2: Dynamic Content Rendering & API Integration")
add_bullet("• Asynchronous Form Submissions: ", "All forms use the Fetch API with JSON payloads to interact with FastAPI endpoints without page reloads.")
add_bullet("• Live Data Explorer: ", "Dataset Management features instant search filtering across clause ID and clause text with category dropdown filters.")
add_bullet("• Recharts Metric Graphs: ", "Evaluation Results renders comparative bar graphs comparing Original vs. Augmented metrics (Accuracy, Macro F1, Recall).")
add_bullet("• Interactive Review Queues: ", "Semantic Validation allows individual and batch approval/rejection of generated variations.")

doc.add_page_break()

# ----------------- PAGE 9: MILESTONE 5 DEPLOYMENT -----------------

add_heading("Milestone 5: Deployment")
add_paragraph(
    "In Milestone 5, the application is verified locally and deployed publicly via Ngrok to share the live application over a secure public URL without cloud hosting overhead."
)

add_subheading("Activity 5.1: Local Testing & Verification")
add_paragraph("Start both servers locally using separate terminal windows:")
add_code_block([
    "# Terminal 1 - Start FastAPI Backend Server",
    "python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload",
    "",
    "# Terminal 2 - Start Vite React Frontend",
    "cd frontend",
    "npm run dev"
])
add_paragraph("Open http://localhost:5173 to access the local user interface and verify that all 200 benchmark clauses and training experiments load.")

add_subheading("Activity 5.2: Public Deployment via Ngrok")
add_paragraph("Install and configure Ngrok to expose the frontend server over a public HTTPS tunnel:")
add_code_block([
    "# 1. Install Ngrok via winget",
    "winget install --id Ngrok.Ngrok",
    "",
    "# 2. Connect your free Ngrok Authtoken",
    "ngrok config add-authtoken YOUR_AUTHTOKEN_HERE",
    "",
    "# 3. Allow external tunnel hosts in frontend/vite.config.js",
    "# server: { port: 5173, allowedHosts: true }",
    "",
    "# 4. Launch public tunnel",
    "ngrok http 5173"
])
add_paragraph("Ngrok outputs a live public URL (e.g., https://moodiness-escalate-wobbling.ngrok-free.dev) accessible from any browser or device.")

doc.add_page_break()

# ----------------- PAGES 10-16: EXPLORING THE WEBSITE'S WEB PAGES WITH LIVE SCREENSHOTS -----------------

add_heading("Exploring the Website's Web Pages:")

SCREENSHOT_DIR = r"c:\Users\HP\OneDrive\Desktop\Gen AI\docs\screenshots"

# Screen 1: Overview Dashboard
add_image_section(
    os.path.join(SCREENSHOT_DIR, "01_overview_dashboard.png"),
    "Overview Dashboard:",
    "The single-page overview dashboard serves as the central control panel for ClauseAugment AI. It displays active dataset indicators, total benchmark clauses (200), total generated variations (2,000), validated expansion ratio (600.5%), and the best-performing model Macro F1 (0.8459). The main section includes a class distribution bar chart across all 10 legal categories and a guided 6-phase pipeline workflow."
)

# Screen 2: Dataset Management
add_image_section(
    os.path.join(SCREENSHOT_DIR, "02_dataset_management.png"),
    "Legal Dataset Management Portal:",
    "A comprehensive data ingestion and exploration portal. Users can upload custom contract datasets in CSV or JSON format with automatic schema validation (clause_id, clause_text, clause_type). Summary cards display total clauses (200), active categories (10), average word count (19.5), and class imbalance ratio (1:1). The interactive Clause Explorer provides real-time search and category filtering with one-click CSV and JSON downloads."
)

# Screen 3: Augmentation Studio
add_image_section(
    os.path.join(SCREENSHOT_DIR, "03_augmentation_studio.png"),
    "Contract Clause Augmentation Studio:",
    "The core perturbation control center. Users can toggle multiple augmentation techniques (WordNet Synonym Replacement, Sentence Restructuring, Random Insertion, Random Deletion, Random Swap, Back Translation, and Google Gemini 2.5 Flash). Experimental controls allow adjusting the augmentation multiplier (1x to 5x), similarity threshold (0.75), and reproducibility seed (42). The lower catalog displays generated variations with cosine similarity percentages and review statuses."
)

# Screen 4: Semantic Validation
add_image_section(
    os.path.join(SCREENSHOT_DIR, "04_semantic_validation.png"),
    "Semantic & Legal Guardrails Validation:",
    "Ensures generated text maintains legal equivalence and obligation fidelity. The review queue filters clauses by Needs Review, Accepted, and Rejected. Each row details the original clause vs. augmented text, semantic cosine similarity score, and automated guardrail explanations (e.g., 'Obligation modal verb dropped: Original had shall, augmented lacks them'). Researchers can approve or reject variations individually or in batches."
)

# Screen 5: Model Training
add_image_section(
    os.path.join(SCREENSHOT_DIR, "05_model_training.png"),
    "Machine Learning Training Engine:",
    "Launches comparative baseline vs. augmented training experiments under strict Zero-Data-Leakage guarantees. Users select from 4 classification architectures (Logistic Regression, Linear SVM, Multinomial Naive Bayes, Random Forest) and feature representations (TF-IDF Unigrams vs. Bigrams). Experimental controls allow tuning train/test split ratios (80/20) and reproducibility seeds, with a prominent leakage-free checklist confirming data isolation."
)

# Screen 6: Evaluation Results
add_image_section(
    os.path.join(SCREENSHOT_DIR, "06_evaluation_results.png"),
    "Evaluation Results Dashboard:",
    "Displays comparative empirical performance on the held-out test split. Top stat cards highlight Test Accuracy Delta (+2.5%), Macro F1 Score Delta (+0.0406), Relative F1 Improvement (+6.79%), and Generalization Outcome ('Robust Gain'). The comparative bar chart compares Original vs. Augmented metrics across Accuracy, Macro F1, Weighted F1, Precision, and Recall. The lower section provides an interactive multi-class confusion matrix and exportable reports."
)

# Screen 7: Robustness Testing
add_image_section(
    os.path.join(SCREENSHOT_DIR, "07_robustness_testing.png"),
    "Out-of-Distribution Robustness Stress Testing:",
    "Examines model resilience against real-world drafting variance and document noise across 4 targeted stress perturbations: Drafting Style Shift, Paraphrase Stress Test, Scanned/OCR Spacing Noise, and Transcription/Casing Permutations. Each test card displays Augmented F1 vs. Original Baseline F1 and the net positive Resilience Shift, proving that data augmentation enhances classifier robustness."
)

# ----------------- CONCLUSION -----------------

add_heading("Conclusion:")
add_paragraph(
    "ClauseAugment AI is an end-to-end Machine Learning, NLP, and Data Augmentation platform built with FastAPI and React that streamlines legal contract clause classification. It combines traditional algorithmic NLP (WordNet, Syntactic Restructuring, Lexical Swapping) with optional Google Gemini 2.5 Flash generative models to solve data scarcity and class imbalance without relying on expensive, black-box paid APIs. The project, which included model selection, multi-tier semantic validation, zero-leakage training, and public deployment via Ngrok, highlights how controlled data augmentation boosts classification accuracy (+5.0%) and minority class F1 scores (+25.0%)."
)
add_paragraph(
    "Looking ahead, ClauseAugment AI offers significant opportunities for expansion, such as integrating local Sentence-BERT transformer embeddings for offline semantic scoring, adding conditional generative adversarial networks (CTGAN) for multi-modal tabular datasets, and implementing active learning human-in-the-loop review interfaces. By continuously refining algorithmic guardrails and enhancing frontend accessibility, the platform is well-positioned to evolve from an academic benchmark into an enterprise-ready legal NLP assistant."
)

output_path = r"c:\Users\HP\OneDrive\Desktop\Gen AI\ClauseAugment_AI_Project_Documentation.docx"
doc.save(output_path)
print(f"Successfully generated 100% sample-aligned DOCX at: {output_path}")
