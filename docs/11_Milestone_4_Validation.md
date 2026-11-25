# Milestone 11: Milestone 4 - Multi-Tier Validation Engine

## 1. Text Semantic & Linguistic Validation
Every generated text variation is checked against 5 automated validation rules:
1. **Cosine Similarity Threshold**: Ensures TF-IDF semantic cosine similarity falls within $[0.60, 0.98]$. Values $< 0.60$ indicate topic drift; values $> 0.98$ indicate lack of variation.
2. **Negation Polarity Preservation**: Scans for negation tokens (`not`, `never`, `neither`, `none`, `without`). Any inversion between original and augmented sentences flags `NEGATION_MISMATCH` and triggers rejection.
3. **Modal Verb & Obligation Integrity**: Ensures vital obligation verbs (`shall`, `must`, `will`) are not removed.
4. **Numerical & Date Entity Retention**: Verifies all numeric figures, financial amounts, and dates are preserved.
5. **Length Drift Boundary**: Confirms token count drift stays within $\pm 40\%$.

---

## 2. Tabular Validation Rules
1. **Dynamic Physical Bounds**: Ensures continuous variables do not exceed observed range extremes by more than $15\%$.
2. **Categorical Domain Integrity**: Verifies synthetic rows do not introduce unobserved discrete categories.
3. **Data Type and Null Checks**: Ensures target types and non-null constraints are respected.
