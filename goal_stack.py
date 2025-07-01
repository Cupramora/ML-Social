# goal_stack.py
# manages prioritized goals, seeded by drives, modulated by self-model

import time
from social_drive_engine import SocialDriveEngine
from self_model import self_model  # if not globally defined, create local instance

drive_engine = SocialDriveEngine()

class Goal:
    def __init__(self, description, priority=0.5):
        self.description = description
        self.created_at = time.time()
        self.priority = priority
        self.status = "active"
        self.history = []

    def promote(self, amount=0.1):
        self.priority = min(1.0, self.priority + amount)
        self.history.append(("promoted", time.time(), self.priority))

    def demote(self, amount=0.1):
        self.priority = max(0.0, self.priority - amount)
        self.history.append(("demoted", time.time(), self.priority))

    def complete(self):
        self.status = "completed"
        self.history.append(("completed", time.time()))

    def fail(self):
        self.status = "failed"
        self.history.append(("failed", time.time()))

class GoalStack:
    def __init__(self):
        self.stack = []

    def check_drive_pressure(self, threshold=0.7):
        should_pulse, motive = drive_engine.should_form_goal(threshold)
        if should_pulse:
            new_goal = f"express {motive} drive"
            self.add_goal(new_goal, priority=0.6)
            drive_engine.reinforce(motive, amount=-0.3)
            return {"new_goal": new_goal, "drive": motive}
        return None

    def add_goal(self, description, priority=0.5):
        # self_model bias (boost if she believes it's a strength)
        for skill in self_model.capabilities:
            if skill in description:
                skill_score = self_model.capabilities[skill]
                priority += 0.15 * (skill_score - 0.5)
                break

        goal = Goal(description, priority)
        self.stack.append(goal)
        self.stack.sort(key=lambda g: -g.priority)
        return goal

    def get_top_goal(self):
        active = [g for g in self.stack if g.status == "active"]
        return active[0] if active else None

    def review_goals(self):
        return [{
            "description": g.description,
            "priority": g.priority,
            "status": g.status,
            "age": round(time.time() - g.created_at, 1)
        } for g in self.stack]
