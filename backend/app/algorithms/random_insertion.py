import random
from typing import List
from backend.app.algorithms.base import BaseAugmenter

SAFE_LEGAL_MODIFIERS = [
    "promptly", "duly", "mutually", "specifically", "formally",
    "reasonably", "expressly", "strictly", "hereby", "in writing"
]

class RandomInsertionAugmenter(BaseAugmenter):
    def __init__(self):
        super().__init__("random_insertion")

    def generate(self, text: str, n: int = 1, seed: int = 42) -> List[str]:
        rng = random.Random(seed)
        words = text.split()
        if len(words) < 5:
            return [text] * n

        results = []
        for i in range(n):
            new_words = list(words)
            # Find safe insertion positions: e.g. directly after modal verbs like "shall", "may", "will", "must"
            safe_positions = []
            for idx, w in enumerate(new_words[:-1]):
                clean = w.lower().strip(",.:;!?'\"")
                if clean in {"shall", "may", "must", "will", "agrees to", "agrees"}:
                    safe_positions.append(idx + 1)

            # If no modal found, find non-protected adjective/adverb positions
            if not safe_positions:
                for idx in range(1, len(new_words) - 1):
                    prev_w = new_words[idx - 1]
                    curr_w = new_words[idx]
                    if not self.is_protected(curr_w, prev_w):
                        safe_positions.append(idx)

            if not safe_positions:
                results.append(text)
                continue

            insert_pos = rng.choice(safe_positions)
            modifier = rng.choice(SAFE_LEGAL_MODIFIERS)
            new_words.insert(insert_pos, modifier)

            results.append(" ".join(new_words))

        return results
