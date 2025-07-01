# belief_registry.py
# tracks what the agent thinks others believe or expect about her

import time

class BeliefRegistry:
    def __init__(self):
        self.beliefs = {}  # { "dane": { "goal_execution": 0.8, "social_awareness": 0.6 }, ... }
        self.timestamps = {}

    def update_belief(self, person, topic, strength):
        if person not in self.beliefs:
            self.beliefs[person] = {}
        self.beliefs[person][topic] = strength
        self.timestamps[(person, topic)] = time.time()

    def get_belief(self, person, topic):
        return self.beliefs.get(person, {}).get(topic, None)

    def summarize_beliefs(self, person):
        summary = f" beliefs about {person}:\n"
        person_beliefs = self.beliefs.get(person, {})
        for topic, value in person_beliefs.items():
            summary += f" - believes my {topic} is at {round(value, 2)}\n"
        return summary if person_beliefs else "no tracked beliefs."

    def detect_belief_gap(self, person, topic, self_score):
        """
        Detect if they believe she's stronger than she feels, or vice versa
        """
        their_score = self.get_belief(person, topic)
        if their_score is None:
            return None
        delta = self_score - their_score
        if abs(delta) > 0.2:
            return {
                "person": person,
                "topic": topic,
                "delta": round(delta, 2),
                "recommendation": "communicate progress" if delta > 0 else "repair misunderstanding"
            }
        return None
