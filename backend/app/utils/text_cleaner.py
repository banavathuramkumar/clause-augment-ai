import re
import unicodedata
from typing import List, Tuple
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from app.config import LEGAL_KEYWORDS, LEGAL_MODAL_VERBS, LEGAL_NEGATIONS

# Initialize standard NLTK components
try:
    NLTK_STOPWORDS = set(stopwords.words("english"))
except Exception:
    NLTK_STOPWORDS = set()

LEMATIZER = WordNetLemmatizer()

# Preserve critical legal particles from stopword removal
CRITICAL_LEGAL_WORDS = LEGAL_MODAL_VERBS.union(LEGAL_NEGATIONS).union({
    "all", "any", "either", "neither", "each", "both", "such", "other",
    "herein", "hereunder", "hereto", "thereof", "whereas", "in", "to", "for", "with", "against", "under"
})

SAFE_STOPWORDS = NLTK_STOPWORDS - CRITICAL_LEGAL_WORDS

def normalize_unicode(text: str) -> str:
    """Normalize unicode characters such as curly quotes, en/em dashes, and ligatures."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    replacements = {
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "--", "\u00a0": " ", "\u2026": "..."
    }
    for char, rep in replacements.items():
        text = text.replace(char, rep)
    return text

def clean_whitespace(text: str) -> str:
    """Strip extraneous whitespace, tabs, and newlines."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()

def safe_sent_tokenize(text: str) -> List[str]:
    try:
        return sent_tokenize(text)
    except Exception:
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
        return sents if sents else [text]

def safe_word_tokenize(text: str) -> List[str]:
    try:
        return word_tokenize(text)
    except Exception:
        return re.findall(r"\w+|[^\w\s]", text)

def clean_legal_text(
    text: str,
    remove_stopwords: bool = False,
    lemmatize: bool = False,
    preserve_legal_terms: bool = True
) -> Tuple[str, List[str], List[str], List[str]]:
    """
    Carefully processes legal clause text without modifying or degrading legal meaning.
    Returns: (processed_text, tokens, sentences, operations_applied)
    """
    operations = []
    
    # 1. Unicode normalization
    text = normalize_unicode(text)
    operations.append("Unicode character normalization")
    
    # 2. Whitespace and formatting cleaning
    text = clean_whitespace(text)
    operations.append("Whitespace and formatting normalization")
    
    # 3. Sentence segmentation
    sentences = safe_sent_tokenize(text)
    operations.append(f"Sentence segmentation ({len(sentences)} sentence(s) identified)")
    
    # 4. Tokenization (preserving punctuation boundaries)
    tokens = safe_word_tokenize(text)
    operations.append(f"Punctuation-aware tokenization ({len(tokens)} tokens)")
    
    filtered_tokens = []
    for token in tokens:
        lower_token = token.lower()
        
        # Check if stopword removal requested
        if remove_stopwords:
            if preserve_legal_terms and (lower_token in CRITICAL_LEGAL_WORDS or lower_token in LEGAL_KEYWORDS):
                pass
            elif lower_token in SAFE_STOPWORDS:
                continue
                
        # Check if lemmatization requested
        if lemmatize:
            if preserve_legal_terms and (lower_token in LEGAL_MODAL_VERBS or lower_token in LEGAL_NEGATIONS):
                filtered_tokens.append(token)
            else:
                try:
                    lemma = LEMATIZER.lemmatize(token)
                    filtered_tokens.append(lemma)
                except Exception:
                    filtered_tokens.append(token)
        else:
            filtered_tokens.append(token)
            
    if remove_stopwords:
        operations.append("Selective non-critical stopword filtering (legal terms protected)")
    if lemmatize:
        operations.append("Controlled lemmatization (modal verbs protected)")
        
    # Reassemble tokens with clean spacing
    processed_text = " ".join(filtered_tokens)
    processed_text = re.sub(r'\s+([,.:;!?"\'])', r'\1', processed_text)
    processed_text = re.sub(r'([(\[\{])\s+', r'\1', processed_text)
    
    return processed_text, filtered_tokens, sentences, operations
