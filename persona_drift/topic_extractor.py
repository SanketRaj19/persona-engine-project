from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List

class TopicExtractor:
    def __init__(self):
        # Using a lightweight approach with English stop words
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5)

    def extract_top_keywords(self, corpus: List[str]) -> List[str]:
        """Extracts the top distinguishing terms for a given day's corpus."""
        if not corpus or all(len(text.strip()) == 0 for text in corpus):
            return ["none"]
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Aggregate tf-idf scores across all documents in this batch
            sums = tfidf_matrix.sum(axis=0).A1
            data = list(zip(feature_names, sums))
            
            # Sort by highest aggregate score
            sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
            return [word for word, score in sorted_data[:3]]
        except Exception:
            # Fallback if vocabulary is too small or all stop words
            words = " ".join(corpus).lower().split()
            valid_words = [w for w in words if len(w) > 3][:3]
            return valid_words if valid_words else ["general-chat"]
