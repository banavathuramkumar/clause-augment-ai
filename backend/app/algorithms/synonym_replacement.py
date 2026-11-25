import random
import re
from typing import List
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from backend.app.algorithms.base import BaseAugmenter

class SynonymReplacementAugmenter(BaseAugmenter):
    def __init__(self):
        super().__init__("synonym_replacement")

    def _get_synonyms(self, word: str) -> List[str]:
        synonyms = set()
        clean_word = word.lower().strip(",.:;!?'\"()[]{}")
        for syn in wordnet.synsets(clean_word):
            for lemma in syn.lemmas():
                name = lemma.name().replace("_", " ")
                # Only use single words that aren't identical and don't match protected terms
                if " " not in name and name.lower() != clean_word and not self.is_protected(name):
                    synonyms.add(name)
        return list(synonyms)

    def generate(self, text: str, n: int = 1, seed: int = 42) -> List[str]:
        rng = random.Random(seed)
        words = text.split()
        if len(words) < 4:
            return [text] * n

        results = []
        for i in range(n):
            candidate_indices = []
            for idx, word in enumerate(words):
                prev_w = words[idx - 1] if idx > 0 else ""
                next_w = words[idx + 1] if idx < len(words) - 1 else ""
                if not self.is_protected(word, prev_w, next_w):
                    syns = self._get_synonyms(word)
                    if syns:
                        candidate_indices.append((idx, syns))

            if not candidate_indices:
                results.append(text)
                continue

            # Replace 1 or 2 eligible words
            num_to_replace = max(1, min(len(candidate_indices), max(1, int(len(words) * 0.15))))
            selected_candidates = rng.sample(candidate_indices, min(num_to_replace, len(candidate_indices)))

            new_words = list(words)
            for idx, syns in selected_candidates:
                orig_word = new_words[idx]
                punct_suffix = ""
                clean_orig = orig_word
                # Preserve trailing punctuation
                m = re.search(r"([,.:;!?'\"]+)$", orig_word)
                if m:
                    punct_suffix = m.group(1)
                    clean_orig = orig_word[: -len(punct_suffix)]

                chosen_syn = rng.choice(syns)
                if clean_orig.isupper():
                    chosen_syn = chosen_syn.upper()
                elif clean_orig and clean_orig[0].isupper():
                    chosen_syn = chosen_syn.capitalize()
                else:
                    chosen_syn = chosen_syn.lower()

                new_words[idx] = chosen_syn + punct_suffix

            var_text = " ".join(new_words)
            results.append(var_text)

        return results

    def augment(self, text: str, n_replacements: int = 1, **kwargs) -> str:
        """Convenience method for backward compatibility."""
        res = self.generate(text, n=1)
        return res[0] if res else text

# Backward compatibility alias
SynonymReplacer = SynonymReplacementAugmenter

