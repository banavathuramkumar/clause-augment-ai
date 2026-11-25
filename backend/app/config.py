import os
from pathlib import Path
import nltk

BASE_DIR = Path(__file__).resolve().parent.parent.parent
WORKSPACE_NLTK = BASE_DIR / "nltk_data"
if WORKSPACE_NLTK.exists():
    nltk.data.path.insert(0, str(WORKSPACE_NLTK))

BACKEND_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BACKEND_DIR / "datasets"
TRAINED_MODELS_DIR = BACKEND_DIR / "trained_models"
EXPORTS_DIR = BACKEND_DIR / "exports"

DATASETS_DIR.mkdir(exist_ok=True)
TRAINED_MODELS_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{BACKEND_DIR / 'clause_augment.db'}"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.0-flash")

ALLOWED_CLAUSE_CATEGORIES = [
    "Confidentiality",
    "Indemnification",
    "Termination",
    "Liability",
    "Governing Law",
    "Payment",
    "Force Majeure",
    "Dispute Resolution",
    "Intellectual Property",
    "Data Protection"
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

LEGAL_MODAL_VERBS = {"shall", "may", "must", "will", "should", "cannot", "agree", "agrees"}

LEGAL_NEGATIONS = {"not", "no", "never", "neither", "nor", "none", "without", "except", "unless"}
