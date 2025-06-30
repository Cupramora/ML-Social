# strategic_reasoner.py

import time
import random

class StrategicReasoner:
    def __init__(self, emotional_state=None):
        self.emotional_state = emotional_state
        self.decision_log = []

    def simulate_outcome(self, goal, context):
        """
        Fake-run a scenario: estimate confidence, risk, and social fit
        """
        # Use emotional_state to bias risk or urgency if available
        mood_bias = self.emotional_state.get_dominant_emotion() if self.emotional_state else "neutral"

        # Example mood modifier logic
        mood_modifiers = {
            "curious": 0.2,
            "anxious": -0.3,
            "confident": 0.3,
            "guilt": -0.2,
            "neutral": 0.0
        }
        bias = mood_modifiers.get(mood_bias, 0.0)

        base_confidence = random.uniform(0.4, 0.7)  # Estimate default
        adjusted_confidence = max(0.0, min(1.0, base_confidence + bias))

        strategy = {
            "goal": goal.description,
            "context": context,
            "confidence": round(adjusted_confidence, 3),
            "risk_estimate": round(1 - adjusted_confidence, 3),
            "mood_bias": mood_bias,
            "timestamp": time.time()
        }

        self.decision_log.append(strategy)
        return strategy

    def review_past_decisions(self, limit=5):
        return self.decision_log[-limit:]
