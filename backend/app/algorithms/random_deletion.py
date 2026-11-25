import random
from typing import List
from backend.app.algorithms.base import BaseAugmenter

REDUNDANT_LEGAL_CANDIDATES = {
    "hereby", "herein", "specifically", "expressly", "duly",
    "actually", "formally", "strictly", "respective", "solely"
}

class RandomDeletionAugmenter(BaseAugmenter):
    def __init__(self):
        super().__init__("random_deletion")

    def generate(self, text: str, n: int = 1, seed: int = 42) -> List[str]:
        rng = random.Random(seed)
        words = text.split()
        if len(words) < 6:
            return [text] * n

        results = []
        for i in range(n):
            new_words = list(words)
            # Find eligible redundant words first
            redundant_indices = [
                idx for idx, w in enumerate(new_words)
                if w.lower().strip(",.:;!?'\"") in REDUNDANT_LEGAL_CANDIDATES
            ]

            if redundant_indices:
                del_idx = rng.choice(redundant_indices)
                # If deleted word carried punctuation, preserve it onto previous word
                deleted_word = new_words[del_idx]
                punct = ""
                for char in [",", ".", ";", ":"]:
                    if char in deleted_word:
                        punct = char
                        break

                del new_words[del_idx]
                if punct and del_idx > 0:
                    new_words[del_idx - 1] = new_words[del_idx - 1].rstrip(",.:;") + punct

                results.append(" ".join(new_words))
            else:
                # If no explicit redundant words, find a non-critical descriptive adverb/adjective
                non_critical_indices = []
                for idx, w in enumerate(new_words):
                    prev_w = new_words[idx - 1] if idx > 0 else ""
                    next_w = new_words[idx + 1] if idx < len(words) - 1 else ""
                    if not self.is_protected(w, prev_w, next_w) and w.lower() not in {"shall", "may", "must", "not", "no"}:
                        non_critical_indices.append(idx)

                if non_critical_indices and len(words) > 8:
                    del_idx = rng.choice(non_critical_indices)
                    del new_words[del_idx]
                    results.append(" ".join(new_words))
                else:
                    results.append(text)

        return results
