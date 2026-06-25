import pickle
import os
import time
from typing import Tuple

class OfflineIntentClassifier:
    def __init__(self, model_path: str = "./model.pkl"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model payload file missing at {model_path}. Run train.py first.")
        with open(model_path, 'rb') as f:
            payload = pickle.load(f)
        self.vectorizer = payload["vectorizer"]
        self.classifier = payload["classifier"]

    def predict(self, text: str) -> Tuple[str, float]:
        """Runs inference and returns (label, confidence_score)."""
        if not text or not text.strip():
            return "unknown", 0.0
            
        # Transform using training vector space bounds
        vectorized_text = self.vectorizer.transform([text])
        
        # Calculate label prediction
        label = self.classifier.predict(vectorized_text)[0]
        
        # Calculate probability distribution for confidence metric
        probs = self.classifier.predict_proba(vectorized_text)[0]
        classes = self.classifier.classes_
        confidence = float(max(probs))
        
        return label, confidence
