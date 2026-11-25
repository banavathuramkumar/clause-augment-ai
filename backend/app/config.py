import os
from pathlib import Path
import nltk
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
WORKSPACE_NLTK = BASE_DIR / "nltk_data"
NLTK_DATA_DIR = WORKSPACE_NLTK
if WORKSPACE_NLTK.exists():
    nltk.data.path.insert(0, str(WORKSPACE_NLTK))

BACKEND_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BACKEND_DIR / "datasets"
TRAINED_MODELS_DIR = BACKEND_DIR / "trained_models"
EXPORTS_DIR = BACKEND_DIR / "exports"

DATASETS_DIR.mkdir(exist_ok=True)
TRAINED_MODELS_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)

PROJECT_NAME = "ClauseAugment AI"
API_V1_STR = "/api"
DATABASE_URL = f"sqlite:///{BACKEND_DIR / 'clause_augment.db'}"

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash").strip()

# Supported universal modalities and tasks
SUPPORTED_MODALITIES = ["text", "tabular", "mixed"]
SUPPORTED_TASKS = ["classification", "regression", "unlabeled"]

MIN_SEMANTIC_SIMILARITY = 0.60
MAX_SEMANTIC_SIMILARITY = 0.98
MAX_LENGTH_RATIO_DIFFERENCE = 0.40

PRESERVED_LEGAL_TERMS = [
    "shall", "indemnify", "indemnification", "confidentiality", "proprietary",
    "termination", "liability", "governing law", "jurisdiction", "force majeure",
    "intellectual property", "arbitration", "warranty", "breach"
]

LEGAL_KEYWORDS = {
    "confidential", "proprietary", "trade secret", "disclosure", "recipient", "disclosing",
    "indemnify", "indemnification", "hold harmless", "defend", "damages", "losses",
    "terminate", "termination", "cure", "breach", "expiration", "notice",
    "liability", "aggregate liability", "indirect", "consequential", "punitive", "warranties",
    "governing law", "jurisdiction", "venue", "courts", "arbitration",
    "payment", "invoice", "taxes", "interest", "delinquent", "fees",
    "force majeure", "acts of god", "epidemic", "strike", "unforeseen",
    "arbitration", "mediator", "arbitrator", "dispute", "litigation", "injunctive",
    "intellectual property", "patent", "copyright", "trademark", "license", "ownership",
    "personal data", "gdpr", "ccpa", "privacy", "security breach", "processing"
}

MODAL_VERBS = {"shall", "may", "must", "will", "should", "cannot", "agree", "agrees"}
NEGATION_WORDS = {"not", "no", "never", "neither", "nor", "none", "without", "except", "unless"}
LEGAL_MODAL_VERBS = MODAL_VERBS
LEGAL_NEGATIONS = NEGATION_WORDS
