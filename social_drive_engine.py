# social_drive_engine.py

import time
import math

class SocialDriveEngine:
    def __init__(self):
        self.drives = {
            "novelty": 0.4,
            "connection": 0.5,
            "resolution": 0.3
        }
        self.last_updated = time.time()

    def decay_drives(self):
        now = time.time()
        dt = now - self.last_updated
        for k in self.drives:
            self.drives[k] = max(0.0, self.drives[k] - 0.01 * dt)
        self.last_updated = now

    def reinforce(self, drive, amount=0.1):
        if drive in self.drives:
            self.drives[drive] = min(1.0, self.drives[drive] + amount)

    def get_dominant_drive(self):
        self.decay_drives()
        return max(self.drives.items(), key=lambda item: item[1])

    def should_form_goal(self, threshold=0.7):
        dom_drive, level = self.get_dominant_drive()
        return level >= threshold, dom_drive
