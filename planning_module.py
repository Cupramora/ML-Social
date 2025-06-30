# planning_module.py

import time

class PlanStep:
    def __init__(self, description, condition=None, fallback=None):
        self.description = description
        self.condition = condition  # optional predicate: "sensor_ready == True"
        self.status = "pending"     # pending, complete, failed
        self.fallback = fallback    # alternate step if this fails
        self.timestamp = time.time()

class Plan:
    def __init__(self, goal):
        self.goal = goal
        self.steps = []
        self.created_at = time.time()
        self.status = "active"

    def add_step(self, description, condition=None, fallback=None):
        step = PlanStep(description, condition, fallback)
        self.steps.append(step)

    def get_next_step(self):
        for step in self.steps:
            if step.status == "pending":
                return step
        return None

    def mark_step_complete(self, index):
        if 0 <= index < len(self.steps):
            self.steps[index].status = "complete"

    def mark_step_failed(self, index):
        if 0 <= index < len(self.steps):
            step = self.steps[index]
            step.status = "failed"
            if step.fallback:
                self.steps.insert(index + 1, PlanStep(step.fallback))
            else:
                self.status = "needs_review"

    def is_complete(self):
        return all(step.status == "complete" for step in self.steps)
