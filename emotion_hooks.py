# emotion_hooks.py
# links emotional_state to drive pressure, goal tuning, and plan shaping

class EmotionHooks:
    def __init__(self, emotional_state, drive_engine):
        self.emotional_state = emotional_state
        self.drive_engine = drive_engine

    def bias_drive_pressure(self):
        mood = self.emotional_state.get_dominant_emotion()
        if mood == "curious":
            self.drive_engine.reinforce("novelty", 0.2)
        elif mood == "lonely":
            self.drive_engine.reinforce("connection", 0.15)
        elif mood == "guilt":
            self.drive_engine.reinforce("resolution", 0.25)

    def modulate_goal_priority(self, goal):
        mood = self.emotional_state.get_dominant_emotion()
        if mood == "anxious" and "connect" in goal.description:
            goal.promote(0.1)
        elif mood == "apathetic":
            goal.demote(0.05)
