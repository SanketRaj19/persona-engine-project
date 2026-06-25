import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure VADER lexicon is downloaded
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

class SentimentWrapper:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        
    def analyze_message(self, text: str) -> float:
        """Returns a compound score between -1.0 (negative) and 1.0 (positive)."""
        if not text or not text.strip():
            return 0.0
        scores = self.sia.polarity_scores(text)
        return scores['compound']
    
    def score_to_tone(self, score: float) -> str:
        if score >= 0.5:
            return "enthusiastic"
        elif 0.1 <= score < 0.5:
            return "curious & formal"
        elif -0.1 < score < 0.1:
            return "neutral"
        elif -0.5 <= score <= -0.1:
            return "casual & frustrated"
        else:
            return "highly distressed"
