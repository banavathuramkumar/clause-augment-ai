"""
Export all augmentation algorithms with standard names and backward-compatible aliases.
"""
from backend.app.algorithms.base import BaseAugmenter
from backend.app.algorithms.synonym_replacement import SynonymReplacementAugmenter, SynonymReplacementAugmenter as SynonymReplacer
from backend.app.algorithms.random_insertion import RandomInsertionAugmenter
from backend.app.algorithms.random_swap import RandomSwapAugmenter
from backend.app.algorithms.random_deletion import RandomDeletionAugmenter
from backend.app.algorithms.sentence_restructuring import SentenceRestructuringAugmenter, SentenceRestructurer
from backend.app.algorithms.back_translation import BackTranslationAugmenter
from backend.app.algorithms.gemini_augmenter import GeminiAugmenter
from backend.app.algorithms.tabular_augmenter import TabularAugmenter
from backend.app.algorithms.transformer_paraphraser import TransformerParaphraser, TransformerParaphraserAugmenter
from backend.app.algorithms.nlpaug_augmenter import NLPAugAugmenter

__all__ = [
    "BaseAugmenter",
    "SynonymReplacementAugmenter",
    "SynonymReplacer",
    "RandomInsertionAugmenter",
    "RandomSwapAugmenter",
    "RandomDeletionAugmenter",
    "SentenceRestructuringAugmenter",
    "SentenceRestructurer",
    "BackTranslationAugmenter",
    "GeminiAugmenter",
    "TabularAugmenter",
    "TransformerParaphraser",
    "TransformerParaphraserAugmenter",
    "NLPAugAugmenter",
]
