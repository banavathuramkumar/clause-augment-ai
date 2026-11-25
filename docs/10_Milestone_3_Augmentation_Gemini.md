# Milestone 10: Milestone 3 - Multi-Algorithm Augmentation & Gemini Integration

## 1. Text Augmentation Algorithms
1. **Synonym Replacement**: Replaces non-critical tokens using WordNet synsets while protecting domain terminology, legal modals (`shall`, `must`), and negation words (`not`, `never`).
2. **Sentence Restructuring**: Inverts conditional clauses (e.g., swapping "If X then Y" into "Y if X") and switches between active and passive constructions.
3. **Random Insertion**: Injects non-conflicting synonyms into plausible token positions.
4. **Random Deletion**: Drops uncritical filler words with controlled probability $p \le 0.1$.
5. **Random Swap**: Transposes word pairs to introduce order noise without losing semantic meaning.
6. **Google Gemini LLM Paraphrasing**:
   - Uses `google-genai` SDK with model `gemini-2.5-flash`.
   - Guided by strict system instructions to preserve factual obligations and sentiment.
   - Graceful fallback: If no API key is provided or the network is blocked, the engine automatically falls back to algorithmic sentence restructuring.

---

## 2. Tabular Augmentation Algorithms
1. **SMOTE**: Generates synthetic samples for minority classification labels using k-nearest neighbors in numerical space.
2. **Random Oversampling with Jitter**: Duplicates minority samples with slight continuous Gaussian noise to prevent exact row duplication.
3. **Gaussian Noise Injection**: Adds $\mathcal{N}(0, \sigma \cdot \text{std})$ noise to continuous features.
4. **Numerical Feature Perturbation**: Bounded scaling within $[1 - \delta, 1 + \delta]$ preserving physical limits.
5. **Categorical Resampling**: Mutates discrete columns according to empirical marginal frequency distributions.
