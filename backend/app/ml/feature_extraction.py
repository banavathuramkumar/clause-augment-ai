from typing import Tuple
from sklearn.feature_extraction.text import TfidfVectorizer

def get_vectorizer(feature_type: str = "tfidf_unigram") -> TfidfVectorizer:
    if feature_type == "tfidf_bigram":
        return TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True,
            stop_words="english"
        )
    else:
        return TfidfVectorizer(
            ngram_range=(1, 1),
            max_features=3000,
            sublinear_tf=True,
            stop_words="english"
        )
