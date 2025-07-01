# strategic_reasoner.py
# simulates outcome confidence using emotion and self-model alignment

import time
import random
from self_model import SelfModel
self_model = SelfModel()

class StrategicReasoner:
    def __init__(self, emotional_state=None):
        self.emotional_state = emotional_state
        self.decision_log = []

    def simulate_outcome(self, goal, context):
        mood_bias = self.emotional_state.get_dominant_emotion() if self.emotional_state else "neutral"

        mood_modifiers = {
            "curious": 0.2,
            "anxious": -0.3,
            "confident": 0.3,
            "guilt": -0.2,
            "neutral": 0.0
        }
        bias = mood_modifiers.get(mood_bias, 0.0)

        base_confidence = random.uniform(0.4, 0.7)
        adjusted_confidence = max(0.0, min(1.0, base_confidence + bias))

        # check if goal aligns with known strengths
        skill_match = 0.5
        for skill in self_model.capabilities:
            if skill in goal.description:
                skill_match = self_model.capabilities[skill]
                break

        # adjust confidence based on skill alignment
        adjusted_confidence = round(
            max(0.0, min(1.0, adjusted_confidence * (0.8 + 0.4 * skill_match))),
            3
        )

        strategy = {
            "goal": goal.description,
            "context": context,
            "confidence": adjusted_confidence,
            "risk_estimate": round(1 - adjusted_confidence, 3),
            "mood_bias": mood_bias,
            "skill_alignment": round(skill_match, 2),
            "timestamp": time.time()
        }

        if adjusted_confidence < 0.3:
            self_model.record_failure("low_confidence_" + goal.description)

        self.decision_log.append(strategy)
        return strategy

    def review_past_decisions(self, limit=5):
        return self.decision_log[-limit:]
