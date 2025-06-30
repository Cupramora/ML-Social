# goal_stack.py

import time

class Goal:
    def __init__(self, description, priority=0.5):
        self.description = description
        self.created_at = time.time()
        self.priority = priority  # 0.0 (idle impulse) to 1.0 (urgent mission)
        self.status = "active"   # active, paused, completed, failed
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

    def add_goal(self, description, priority=0.5):
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
