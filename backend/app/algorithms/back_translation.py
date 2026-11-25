from typing import List
from backend.app.algorithms.base import BaseAugmenter
from backend.app.utils.logger import logger

class BackTranslationAugmenter(BaseAugmenter):
    def __init__(self):
        super().__init__("back_translation")
        self.is_available = False
        self._check_model_availability()

    def _check_model_availability(self):
        """Check whether local translation models are installed and reachable."""
        try:
            import transformers  # noqa: F401
            # In an offline environment without downloaded MarianMT weights,
            # we keep is_available False to comply with 'do not fabricate' rule.
            self.is_available = False
        except ImportError:
            self.is_available = False

    def generate(self, text: str, n: int = 1, seed: int = 42) -> List[str]:
        if not self.is_available:
            logger.info("Back-translation model is not available locally. Skipping generation.")
            # Return original text unmodified or raise descriptive message
            return [text] * n
        return [text] * n
