import abc
import re
from typing import List, Set
from nltk.corpus import wordnet
from backend.app.config import LEGAL_KEYWORDS, LEGAL_MODAL_VERBS, LEGAL_NEGATIONS

class BaseAugmenter(abc.ABC):
    def __init__(self, name: str):
        self.name = name
        self.protected_keywords: Set[str] = {w.lower() for w in LEGAL_KEYWORDS}
        self.protected_modals: Set[str] = {w.lower() for w in LEGAL_MODAL_VERBS}
        self.protected_negations: Set[str] = {w.lower() for w in LEGAL_NEGATIONS}
        
    def is_protected(self, word: str, prev_word: str = "", next_word: str = "") -> bool:
        """Determines if a word is legally sensitive and must NOT be altered."""
        w_lower = word.lower().strip(",.:;!?'\"()[]{}")
        
        # Check empty or short
        if not w_lower or len(w_lower) <= 2:
            return True
            
        # Check numbers, currencies, dates
        if re.search(r"\d", word) or "$" in word or "%" in word or "/" in word:
            return True
            
        # Check legal modals and negations
        if w_lower in self.protected_modals or w_lower in self.protected_negations:
            return True
            
        # Check legal domain keywords
        if w_lower in self.protected_keywords:
            return True
            
        # Defined terms (Capitalized in the middle of sentences)
        if word[0].isupper() and prev_word and not prev_word.endswith((".", "!", "?")):
            return True
            
        # Parties or defined roles
        if w_lower in {"party", "parties", "customer", "vendor", "contractor", "client", "licensor", "licensee", "company"}:
            return True
            
        return False

    @abc.abstractmethod
    def generate(self, text: str, n: int = 1, seed: int = 42) -> List[str]:
        """Generate n variations of the input clause text."""
        pass
