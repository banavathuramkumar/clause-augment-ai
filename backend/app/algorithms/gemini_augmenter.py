"""
Gemini context-aware text augmenter using Google GenAI SDK.
Gracefully falls back to algorithmic paraphrase or reports unavailability if GEMINI_API_KEY is not set.
"""
from typing import List, Optional
import os
from backend.app.config import GEMINI_API_KEY, GEMINI_MODEL_NAME
from backend.app.algorithms.base import BaseAugmenter
from backend.app.algorithms.sentence_restructuring import SentenceRestructuringAugmenter

class GeminiAugmenter(BaseAugmenter):
    def __init__(self, model_name: str = GEMINI_MODEL_NAME):
        super().__init__(name="gemini_context_aware")
        self.model_name = model_name
        self.client = None
        self.is_available = False
        
        api_key = GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
        if api_key and api_key != "your_gemini_api_key_here":
            try:
                from google import genai
                self.client = genai.Client(api_key=api_key)
                self.is_available = True
            except Exception as e:
                self.is_available = False
                self.init_error = str(e)
        else:
            self.init_error = "GEMINI_API_KEY not configured"

    def generate(self, text: str, n: int = 1, seed: int = 42) -> List[str]:
        """Generate n variations using Gemini context-aware paraphrasing."""
        return [self.augment(text) for _ in range(n)]

    def augment(self, text: str, domain_context: str = "general", **kwargs) -> str:
        """
        Augment a single text prompt using Gemini API.
        If unavailable, falls back to sentence restructuring / synonym variant.
        """
        if not self.is_available or not self.client:
            restructurer = SentenceRestructuringAugmenter()
            return restructurer.augment(text)

        prompt = (
            f"You are a professional NLP data augmentation assistant. "
            f"Paraphrase the following {domain_context} text while strictly preserving its core factual meaning, "
            f"legal/technical obligations, entity names, numbers, and sentiment. "
            f"Output ONLY the paraphrased text with no quotation marks, introductions, or markdown.\n\n"
            f"Original text: {text}\n"
            f"Paraphrased text:"
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            paraphrased = response.text.strip() if response.text else text
            if paraphrased.startswith(('"', "'")) and paraphrased.endswith(('"', "'")):
                paraphrased = paraphrased[1:-1].strip()
            return paraphrased if paraphrased else text
        except Exception:
            return SentenceRestructuringAugmenter().augment(text)

