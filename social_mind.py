# social_mind.py

import time
from belief_registry import BeliefRegistry
beliefs = BeliefRegistry()

class SocialMind:
    def __init__(self):
        self.agents = {}  # holds social models keyed by name

    def update_agent_model(self, name, feedback):
        """Updates internal social model for an agent based on feedback"""
        model = self.agents.get(name, {
            "preferences": {},
            "interaction_log": [],
            "confusion_triggers": [],
            "emotional_resonance": {},
        })

        if "confused_by" in feedback:
            model["confusion_triggers"].append(feedback["confused_by"])
        if "preferred_style" in feedback:
            model["preferences"].update(feedback["preferred_style"])
        if "emotion" in feedback:
            e = feedback["emotion"]
            model["emotional_resonance"][e] = model["emotional_resonance"].get(e, 0) + 1

        model["interaction_log"].append({
            "timestamp": time.time(),
            "feedback": feedback
        })

        self.agents[name] = model

    def get_agent_summary(self, name):
        """Summarizes known social data about an agent"""
        if name not in self.agents:
            return f"No model available for agent '{name}'"
        
        model = self.agents[name]
        return {
            "preferences": model["preferences"],
            "top_emotions": sorted(model["emotional_resonance"].items(), key=lambda x: -x[1])[:3],
            "confusion_triggers": model["confusion_triggers"][-3:]
        }

    def evaluate_capsule_socially(self, capsule, agent="dane"):
        """Analyzes a capsule in the context of a specific agent's model"""
        model = self.agents.get(agent, {})
        risks = []

        context = capsule.context.lower()
        for trigger in model.get("confusion_triggers", []):
            if trigger.lower() in context:
                risks.append(trigger)

        suggested_mood = "neutral"
        if "nostalgic" in capsule.emotion_vector:
            suggested_mood = "nostalgic"
        elif "anxious" in capsule.emotion_vector:
            suggested_mood = "reassuring"
            # learn belief cues from capsule feedback
        if capsule.feedback == "positive":
            beliefs.update_belief(agent, "social_response", 0.7)
        elif capsule.feedback == "uncertain":
            beliefs.update_belief(agent, "trust_in_strategy", 0.5)
        elif capsule.feedback == "negative":
            beliefs.update_belief(agent, "reasoning_accuracy", 0.3)
        return {
            "social_trust": beliefs.get_belief(agent, "social_response"),
            "belief_gap": beliefs.detect_belief_gap(agent, "reasoning_accuracy", self_score=0.6),
            "agent": agent,
            "risk_of_confusion": bool(risks),
            "triggers_detected": risks,
            "suggested_mood": suggested_mood
        }
