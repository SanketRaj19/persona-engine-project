from typing import Dict, Any

class TriggerDetector:
    def __init__(self):
        pass

    def detect_trigger(self, current_day_data: Dict[str, Any], previous_day_data: Dict[str, Any] = None) -> str:
        """
        Compares consecutive days to flag drift triggers based on dramatic tone shifts 
        or high-ranking topics.
        """
        if not previous_day_data:
            return "Baseline established"

        prev_tone = previous_day_data.get("tone")
        curr_tone = current_day_data.get("tone")
        curr_keywords = current_day_data.get("keywords", [])

        if prev_tone != curr_tone:
            # Shift detected. Determine cause from keywords or extreme sentiment swings
            trigger_context = ", ".join(curr_keywords)
            return f"Shift from [{prev_tone}] to [{curr_tone}] triggered by discussion around: {trigger_context}"
        
        return "No significant drift"
