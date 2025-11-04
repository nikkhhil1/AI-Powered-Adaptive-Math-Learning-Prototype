import pandas as pd
import os
from datetime import datetime

class PerformanceTracker:
    def __init__(self, user="Learner"):  # <-- two underscores before and after init
        self.user = user
        self.attempts = []  # list of dicts

    def log_attempt(self, puzzle, correct: bool, time_taken: float, difficulty: str):
        rec = {
            "timestamp": datetime.utcnow().isoformat(),
            "user": self.user,
            "difficulty": difficulty,
            "prompt": puzzle.prompt,
            "answer": puzzle.answer,
            "correct": bool(correct),
            "time_taken": float(time_taken)
        }
        self.attempts.append(rec)

    def to_dataframe(self):
        return pd.DataFrame(self.attempts)

    def save_csv(self, folder="logs"):
        df = self.to_dataframe()
        os.makedirs(folder, exist_ok=True)
        name = f"{self.user.replace(' ','')}{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.csv"
        path = os.path.join(folder, name)
        df.to_csv(path, index=False)
        return path
# Let's simulate a simple "puzzle" object
class DummyPuzzle:
    def __init__(self):
        self.prompt = "2 + 2 = ?"
        self.answer = "4"

puzzle = DummyPuzzle()

tracker = PerformanceTracker(input("Enter the user name"))
tracker.log_attempt(puzzle, correct=True, time_taken=2.5, difficulty="Easy")
path = tracker.save_csv()
print("File saved at:", path)
print("\nDataFrame Preview:\n")
print(tracker.to_dataframe())
