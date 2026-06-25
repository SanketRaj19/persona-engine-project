import json
import os
from datetime import datetime
from sentiment import SentimentWrapper
from topic_extractor import TopicExtractor
from trigger_detector import TriggerDetector

class DriftEngine:
    def __init__(self):
        self.sentiment_analyzer = SentimentWrapper()
        self.topic_extractor = TopicExtractor()
        self.trigger_detector = TriggerDetector()

    def run_pipeline(self, persona_input_path: str, output_timeline_path: str):
        if not os.path.exists(persona_input_path):
            raise FileNotFoundError(f"Input file not found: {persona_input_path}")
            
        with open(persona_input_path, 'r') as f:
            data = json.load(f)
        
        # Expecting structure: {"history": [{"day": 1, "messages": [...]}, ...]}
        history = data.get("history", [])
        timeline = {}
        previous_day_metrics = None

        for record in sorted(history, key=lambda x: x['day']):
            day_num = record['day']
            messages = record['messages']
            
            # 1. Parse & Sentiment Aggregate
            scores = [self.sentiment_analyzer.analyze_message(m) for m in messages]
            avg_score = sum(scores) / len(scores) if scores else 0.0
            tone = self.sentiment_analyzer.score_to_tone(avg_score)
            
            # 2. Extract Topics (TF-IDF)
            keywords = self.topic_extractor.extract_top_keywords(messages)
            
            current_day_metrics = {
                "day": day_num,
                "avg_sentiment": round(avg_score, 3),
                "tone": tone,
                "keywords": keywords
            }
            
            # 3. Detect Trigger
            trigger = self.trigger_detector.detect_trigger(current_day_metrics, previous_day_metrics)
            current_day_metrics["trigger"] = trigger
            
            timeline[f"Day {day_num}"] = current_day_metrics
            previous_day_metrics = current_day_metrics

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_timeline_path), exist_ok=True)
        with open(output_timeline_path, 'w') as f:
            json.dump(timeline, f, indent=4)
            
        print(f"Timeline successfully outputted to: {output_timeline_path}")

if __name__ == "__main__":
    # Local execution test stub
    engine = DriftEngine()
    # Assuming relative paths mapping to your workspace diagram
    engine.run_pipeline("../data/persona.json", "../data/timeline.json")
