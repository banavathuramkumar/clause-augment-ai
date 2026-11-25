import random
import re
from typing import List
from app.algorithms.base import BaseAugmenter

class RandomSwapAugmenter(BaseAugmenter):
    def __init__(self):
        super().__init__("random_swap")

    def generate(self, text: str, n: int = 1, seed: int = 42) -> List[str]:
        rng = random.Random(seed)
        words = text.split()
        if len(words) < 5:
            return [text] * n

        results = []
        for i in range(n):
            new_words = list(words)
            # Strategy 1: Look for coordinate clauses: "X and Y" or "X or Y"
            coord_indices = []
            for idx in range(1, len(new_words) - 1):
                mid = new_words[idx].lower()
                if mid in {"and", "or"}:
                    w_before = new_words[idx - 1].strip(",.:;!'\"")
                    w_after = new_words[idx + 1].strip(",.:;!'\"")
                    # Make sure neither is a critical modal or negation
                    if (w_before.lower() not in self.protected_modals and 
                        w_before.lower() not in self.protected_negations and
                        w_after.lower() not in self.protected_modals and 
                        w_after.lower() not in self.protected_negations):
                        coord_indices.append(idx)

            if coord_indices:
                chosen_idx = rng.choice(coord_indices)
                # Swap w[chosen_idx-1] and w[chosen_idx+1], preserving punctuation on the latter
                w1 = new_words[chosen_idx - 1]
                w2 = new_words[chosen_idx + 1]

                punct2 = ""
                m2 = re.search(r"([,.:;!?'\"]+)$", w2)
                if m2:
                    punct2 = m2.group(1)
                    w2 = w2[: -len(punct2)]

                punct1 = ""
                m1 = re.search(r"([,.:;!?'\"]+)$", w1)
                if m1:
                    punct1 = m1.group(1)
                    w1 = w1[: -len(punct1)]

                new_words[chosen_idx - 1] = w2 + punct1
                new_words[chosen_idx + 1] = w1 + punct2
                results.append(" ".join(new_words))
            else:
                # Strategy 2: Swap two adjacent non-protected modifiers
                candidate_pairs = []
                for idx in range(len(new_words) - 1):
                    w1 = new_words[idx]
                    w2 = new_words[idx + 1]
                    if not self.is_protected(w1) and not self.is_protected(w2):
                        if not w1.endswith((".", ";", ":", "!")):
                            candidate_pairs.append(idx)

                if candidate_pairs:
                    swap_idx = rng.choice(candidate_pairs)
                    new_words[swap_idx], new_words[swap_idx + 1] = new_words[swap_idx + 1], new_words[swap_idx]
                    results.append(" ".join(new_words))
                else:
                    results.append(text)

        return results
