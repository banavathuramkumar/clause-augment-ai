import re
import json
from typing import Dict, Any, List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.app.config import LEGAL_KEYWORDS, LEGAL_MODAL_VERBS, LEGAL_NEGATIONS

class SemanticValidationEngine:
    def __init__(self, default_threshold: float = 0.75):
        self.default_threshold = default_threshold
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.nlp = None
        self._init_spacy()

    def _init_spacy(self):
        try:
            import spacy
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except Exception:
                self.nlp = spacy.blank("en")
        except Exception:
            self.nlp = None

    def extract_entities(self, text: str) -> List[str]:
        """Extracts named entities (parties, organizations, jurisdictions, money, dates) using spaCy."""
        if not self.nlp:
            return []
        try:
            doc = self.nlp(text)
            return [ent.text.lower() for ent in doc.ents if ent.label_ in {"ORG", "PERSON", "GPE", "DATE", "MONEY"}]
        except Exception:
            return []

    def compute_diversity_metrics(self, orig_text: str, aug_text: str) -> Dict[str, float]:
        """Measures lexical and structural phrasing diversity."""
        w_orig = orig_text.split()
        w_aug = aug_text.split()
        len_orig = len(w_orig)
        len_aug = len(w_aug)
        length_ratio = round(len_aug / max(1, len_orig), 3)

        set1 = set(w.lower() for w in w_orig)
        set2 = set(w.lower() for w in w_aug)
        jaccard_distance = round(1.0 - (len(set1 & set2) / max(1, len(set1 | set2))), 3)
        return {
            "length_ratio": length_ratio,
            "lexical_diversity": jaccard_distance,
            "structural_edit_distance": round(abs(len_orig - len_aug) / max(1, len_orig), 3)
        }

    def compute_similarity(self, orig_text: str, aug_text: str) -> float:
        """Computes TF-IDF cosine similarity between original and augmented text."""
        try:
            tfidf = self.vectorizer.fit_transform([orig_text, aug_text])
            score = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
            return round(score, 4)
        except Exception:
            # Fallback to word-level Jaccard similarity if TF-IDF fails (e.g. empty)
            set1 = set(orig_text.lower().split())
            set2 = set(aug_text.lower().split())
            if not set1 or not set2:
                return 0.0
            return round(len(set1 & set2) / len(set1 | set2), 4)

    def extract_numbers_and_dates(self, text: str) -> List[str]:
        """Extract all numeric representations, percentages, currencies, and numerals."""
        matches = re.findall(r"\b(?:\d+(?:\.\d+)?|\([0-9]+\)|(?:one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|sixty|ninety))\b|[%$]", text, re.IGNORECASE)
        return [m.lower() for m in matches]

    def extract_negations(self, text: str) -> List[str]:
        """Extract negation particles from text."""
        words = re.findall(r"\b\w+\b", text.lower())
        return [w for w in words if w in LEGAL_NEGATIONS]

    def extract_modals(self, text: str) -> List[str]:
        """Extract legal modal verbs from text."""
        words = re.findall(r"\b\w+\b", text.lower())
        return [w for w in words if w in LEGAL_MODAL_VERBS]

    def extract_legal_keywords(self, text: str) -> List[str]:
        """Extract domain legal keywords present in text."""
        text_lower = text.lower()
        found = []
        for kw in LEGAL_KEYWORDS:
            if kw in text_lower:
                found.append(kw)
        return found

    def validate(
        self,
        orig_text: str,
        aug_text: str,
        threshold: float = 0.75,
        enforce_negations: bool = True,
        enforce_modals: bool = True,
        enforce_keywords: bool = True,
        enforce_numbers: bool = True
    ) -> Dict[str, Any]:
        """
        Validates an augmented clause against its original version.
        Returns:
            dict containing similarity_score, flags, booleans, status, and reason.
        """
        flag_reasons: List[str] = []
        
        # 1. Exact Duplicate Detection
        if orig_text.strip().lower() == aug_text.strip().lower():
            flag_reasons.append("Trivial duplicate: Augmented text is identical to original clause.")
            return {
                "similarity_score": 1.0,
                "legal_keywords_preserved": True,
                "negation_preserved": True,
                "modal_verbs_preserved": True,
                "numbers_dates_preserved": True,
                "status": "Rejected",
                "flag_reasons": flag_reasons,
                "reason": "; ".join(flag_reasons)
            }

        # 2. Semantic Similarity Score
        similarity = self.compute_similarity(orig_text, aug_text)

        # 3. Numeric & Date Preservation
        orig_nums = self.extract_numbers_and_dates(orig_text)
        aug_nums = self.extract_numbers_and_dates(aug_text)
        numbers_preserved = True
        if enforce_numbers and orig_nums:
            if set(orig_nums) != set(aug_nums):
                numbers_preserved = False
                flag_reasons.append(f"Numeric/Date discrepancy detected: Original had {orig_nums}, augmented has {aug_nums}.")

        # 4. Negation Preservation
        orig_negs = self.extract_negations(orig_text)
        aug_negs = self.extract_negations(aug_text)
        negation_preserved = True
        if enforce_negations:
            if sorted(orig_negs) != sorted(aug_negs):
                negation_preserved = False
                flag_reasons.append(f"Legal negation alteration: Original negations {orig_negs} vs Augmented {aug_negs}.")

        # 5. Modal Verb Preservation
        orig_modals = self.extract_modals(orig_text)
        aug_modals = self.extract_modals(aug_text)
        modals_preserved = True
        if enforce_modals and orig_modals:
            # Check if any original modal was completely dropped
            if not set(orig_modals).intersection(set(aug_modals)):
                modals_preserved = False
                flag_reasons.append(f"Obligation modal verb dropped: Original had {orig_modals}, augmented lacks them.")

        # 6. Legal Keyword Preservation
        orig_kws = self.extract_legal_keywords(orig_text)
        aug_kws = self.extract_legal_keywords(aug_text)
        keywords_preserved = True
        if enforce_keywords and orig_kws:
            missing_kws = set(orig_kws) - set(aug_kws)
            if missing_kws:
                keywords_preserved = False
                flag_reasons.append(f"Core legal terms eliminated: {list(missing_kws)}.")

        # 7. Determine Final Status
        if not numbers_preserved or not negation_preserved:
            status = "Rejected"
        elif similarity < (threshold - 0.20):
            flag_reasons.append(f"Similarity score ({similarity:.2f}) is significantly below threshold ({threshold:.2f}).")
            status = "Rejected"
        elif not modals_preserved or not keywords_preserved or similarity < threshold:
            if similarity < threshold:
                flag_reasons.append(f"Similarity score ({similarity:.2f}) is slightly below target threshold ({threshold:.2f}).")
            status = "Needs Review"
        else:
            status = "Accepted"

        reason_str = "; ".join(flag_reasons) if flag_reasons else "All legal constraints and semantic thresholds met."

        # Compute diversity
        div = self.compute_diversity_metrics(orig_text, aug_text)

        return {
            "similarity_score": similarity,
            "legal_keywords_preserved": keywords_preserved,
            "negation_preserved": negation_preserved,
            "modal_verbs_preserved": modals_preserved,
            "numbers_dates_preserved": numbers_preserved,
            "lexical_diversity": div["lexical_diversity"],
            "structural_diversity": div["structural_edit_distance"],
            "status": status,
            "flag_reasons": flag_reasons,
            "reason": reason_str
        }

    def validate_text_pair(self, orig_text: str, aug_text: str, threshold: float = 0.6) -> Dict[str, Any]:
        """Convenience method for unit testing and direct pair validation."""
        res = self.validate(orig_text, aug_text, threshold=threshold)
        flags = []
        if not res["negation_preserved"]:
            flags.append("NEGATION_MISMATCH")
        if not res["numbers_dates_preserved"]:
            flags.append("NUMBER_MISMATCH")
        if not res["modal_verbs_preserved"]:
            flags.append("MODAL_MISMATCH")

        return {
            "is_valid": res["status"] in {"Accepted", "Needs Review"},
            "similarity_score": res["similarity_score"],
            "flags": flags,
            "status": res["status"]
        }

validation_engine = SemanticValidationEngine()
ValidationService = SemanticValidationEngine

