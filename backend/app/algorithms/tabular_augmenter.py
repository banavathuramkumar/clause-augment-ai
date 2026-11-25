"""
Tabular data augmentation algorithms:
- Random Oversampling (with optional jitter)
- Bootstrap Sampling
- SMOTE (Synthetic Minority Over-sampling Technique via imbalanced-learn)
- Gaussian Noise Injection for numerical columns
- Numerical Feature Perturbation (bounded +/- %)
- Categorical Resampling from empirical distribution
"""
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import random

class TabularAugmenter:
    """Universal tabular data augmentation engine."""

    def __init__(self):
        pass

    def random_oversample(
        self,
        df: pd.DataFrame,
        target_col: Optional[str] = None,
        samples_per_class: Optional[int] = None,
        jitter_factor: float = 0.02,
        numerical_cols: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Oversamples rows, optionally targeting minority classes and adding slight numerical jitter."""
        if df.empty:
            return df

        num_cols = numerical_cols or df.select_dtypes(include=[np.number]).columns.tolist()
        
        if target_col and target_col in df.columns:
            counts = df[target_col].value_counts()
            max_count = counts.max() if not samples_per_class else samples_per_class
            augmented_dfs = [df.copy()]

            for label, count in counts.items():
                diff = max_count - count
                if diff > 0:
                    subset = df[df[target_col] == label]
                    sampled = subset.sample(n=diff, replace=True)
                    if jitter_factor > 0 and num_cols:
                        sampled = self.inject_gaussian_noise(sampled, num_cols, std_dev=jitter_factor)
                    augmented_dfs.append(sampled)
            return pd.concat(augmented_dfs, ignore_index=True)
        else:
            # Unsupervised row oversampling
            n_samples = max(1, int(len(df) * 0.5))
            sampled = df.sample(n=n_samples, replace=True).copy()
            if jitter_factor > 0 and num_cols:
                sampled = self.inject_gaussian_noise(sampled, num_cols, std_dev=jitter_factor)
            return pd.concat([df, sampled], ignore_index=True)

    def bootstrap_sample(
        self,
        df: pd.DataFrame,
        sample_ratio: float = 0.5,
        target_col: Optional[str] = None
    ) -> pd.DataFrame:
        """Generates bootstrap replicas with replacement."""
        if df.empty:
            return df
        n = max(1, int(len(df) * sample_ratio))
        return df.sample(n=n, replace=True)

    def inject_gaussian_noise(
        self,
        df: pd.DataFrame,
        numerical_cols: List[str],
        std_dev: float = 0.05
    ) -> pd.DataFrame:
        """Adds zero-mean Gaussian noise scaled by column standard deviation to numerical columns."""
        res_df = df.copy()
        for col in numerical_cols:
            if col in res_df.columns:
                series = pd.to_numeric(res_df[col], errors='coerce')
                col_std = series.std(skipna=True)
                if pd.isna(col_std) or col_std == 0:
                    col_std = 1.0
                noise = np.random.normal(0, std_dev * col_std, size=len(res_df))
                new_vals = series + noise
                # If original was integer, round
                if pd.api.types.is_integer_dtype(df[col].dtype):
                    res_df[col] = np.round(new_vals).astype(int)
                else:
                    res_df[col] = np.round(new_vals, 4)
        return res_df

    def perturb_numerical(
        self,
        df: pd.DataFrame,
        numerical_cols: List[str],
        perturbation_range: float = 0.08
    ) -> pd.DataFrame:
        """Perturbs numerical features by a random factor within [-perturbation_range, +perturbation_range]."""
        res_df = df.copy()
        for col in numerical_cols:
            if col in res_df.columns:
                series = pd.to_numeric(res_df[col], errors='coerce')
                factors = np.random.uniform(1.0 - perturbation_range, 1.0 + perturbation_range, size=len(res_df))
                new_vals = series * factors
                if pd.api.types.is_integer_dtype(df[col].dtype):
                    res_df[col] = np.round(new_vals).astype(int)
                else:
                    res_df[col] = np.round(new_vals, 4)
        return res_df

    def resample_categorical(
        self,
        df: pd.DataFrame,
        categorical_cols: List[str],
        mutation_rate: float = 0.1
    ) -> pd.DataFrame:
        """Perturbs categorical values with probability mutation_rate based on empirical distribution."""
        res_df = df.copy()
        for col in categorical_cols:
            if col in res_df.columns:
                vals = df[col].dropna().values
                if len(vals) == 0:
                    continue
                mask = np.random.rand(len(res_df)) < mutation_rate
                res_df.loc[mask, col] = np.random.choice(vals, size=mask.sum())
        return res_df

    def smote_oversample(
        self,
        df: pd.DataFrame,
        target_col: str,
        numerical_cols: List[str],
        categorical_cols: Optional[List[str]] = None,
        k_neighbors: int = 3
    ) -> pd.DataFrame:
        """
        Applies SMOTE (Synthetic Minority Over-sampling Technique) to tabular classification datasets.
        Falls back to jittered random oversampling if class sizes are smaller than k_neighbors.
        """
        if target_col not in df.columns:
            return df

        # Remove rows where target or features are completely NaN
        clean_df = df.dropna(subset=[target_col] + numerical_cols).copy()
        counts = clean_df[target_col].value_counts()
        min_class_count = counts.min()

        if min_class_count <= 1:
            # Cannot run SMOTE with only 1 sample in a class, use random oversample with jitter
            return self.random_oversample(df, target_col=target_col, jitter_factor=0.03, numerical_cols=numerical_cols)

        # Dynamic neighbor count
        actual_k = min(k_neighbors, min_class_count - 1)
        if actual_k < 1:
            return self.random_oversample(df, target_col=target_col, jitter_factor=0.03, numerical_cols=numerical_cols)

        try:
            from imblearn.over_sampling import SMOTE
            X_num = clean_df[numerical_cols].values
            y = clean_df[target_col].values

            smote = SMOTE(k_neighbors=actual_k, random_state=42)
            X_res, y_res = smote.fit_resample(X_num, y)

            # Reconstruct DataFrame
            res_df = pd.DataFrame(X_res, columns=numerical_cols)
            res_df[target_col] = y_res

            # For categorical or ID columns not in numerical, sample matching class rows
            other_cols = [c for c in df.columns if c not in numerical_cols and c != target_col]
            if other_cols:
                # Fill missing attributes by sampling from the original class distributions
                class_groups = df.groupby(target_col)
                other_rows = []
                for label in y_res:
                    if label in class_groups.groups:
                        sampled_row = class_groups.get_group(label)[other_cols].sample(1).iloc[0].to_dict()
                        other_rows.append(sampled_row)
                    else:
                        other_rows.append({c: None for c in other_cols})
                other_df = pd.DataFrame(other_rows)
                for col in other_cols:
                    res_df[col] = other_df[col].values

            return res_df
        except Exception:
            # Fallback to jittered oversampling
            return self.random_oversample(df, target_col=target_col, jitter_factor=0.03, numerical_cols=numerical_cols)
