# self_model.py
# tracks internal strengths, weaknesses, recurring patterns, and self-reflection history

import time

class SelfModel:
    def __init__(self):
        self.capabilities = {
            "tone_matching": 0.6,
            "memory_linking": 0.7,
            "risk_prediction": 0.5
        }
        self.reflection_log = []  # records internal observations and identity tags
        self.failures = {}        # { "ambiguous_feedback": 3, ... }

    def update_capability(self, skill, delta):
        current = self.capabilities.get(skill, 0.5)
        updated = max(0.0, min(1.0, current + delta))
        self.capabilities[skill] = updated

    def record_failure(self, tag):
        self.failures[tag] = self.failures.get(tag, 0) + 1

    def log_reflection(self, note):
        self.reflection_log.append({
            "note": note,
            "timestamp": time.time()
        })

    def identity_summary(self):
        summary = "🧠 self-identity profile:\n"
        summary += "- key strengths:\n"
        for skill, score in self.capabilities.items():
            if score > 0.7:
                summary += f"  * {skill}: {round(score, 2)}\n"
        summary += "- recurring breakdowns:\n"
        for tag, count in self.failures.items():
            if count > 2:
                summary += f"  * {tag}: {count} times\n"
        return summary
