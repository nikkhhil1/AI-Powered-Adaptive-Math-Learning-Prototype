
import random
import time

# Puzzle Generator

class PuzzleGenerator:
    def generate(self, level):
        if level == "Easy":
            a, b = random.randint(1, 10), random.randint(1, 10)
        elif level == "Medium":
            a, b = random.randint(10, 50), random.randint(10, 50)
        else:
            a, b = random.randint(50, 100), random.randint(50, 100)

        answer = a + b

        class Puzzle:
            def __init__(self, prompt, answer):
                self.prompt = prompt
                self.answer = answer

            def check_answer(self, user_ans):
                return user_ans == self.answer

        return Puzzle(f"What is {a} + {b}?", answer)


# -------------------------------
# Performance Tracker
# -------------------------------
class PerformanceTracker:
    def __init__(self, user):
        self.user = user
        self.records = []

    def log_attempt(self, puzzle, correct, time_taken, level):
        self.records.append({
            "prompt": puzzle.prompt,
            "correct": correct,
            "time": round(time_taken, 2),
            "level": level
        })

    def summary(self):
        total = len(self.records)
        correct = sum(1 for r in self.records if r["correct"])
        avg_time = sum(r["time"] for r in self.records) / total if total else 0
        return total, correct, avg_time


# -------------------------------
# Adaptive Engine
# -------------------------------
class AdaptiveEngine:
    def __init__(self, initial_level="Easy"):
        self.levels = ["Easy", "Medium", "Hard"]
        self.current_level = initial_level

    def update(self, correct, response_time):
        idx = self.levels.index(self.current_level)
        if correct and response_time < 10 and idx < 2:
            self.current_level = self.levels[idx + 1]
        elif not correct and idx > 0:
            self.current_level = self.levels[idx - 1]


# -------------------------------
# Main program
# -------------------------------
def choose_initial_difficulty():
    options = {"1": "Easy", "2": "Medium", "3": "Hard"}
    while True:
        print("Choose initial difficulty:")
        print("  1) Easy\n  2) Medium\n  3) Hard")
        choice = input("Enter 1/2/3: ").strip()
        if choice in options:
            return options[choice]
        print("Invalid choice, try again.\n")


def main():
    print("AI-Powered Adaptive Math Learning Prototype")
    name = input("Enter learner name: ")
    initial = choose_initial_difficulty()
    rounds = input("How many puzzles this session? (default 5): ").strip()

    try:
        rounds = int(rounds)
        if rounds <= 0:
            rounds = 5
    except:
        rounds = 5

    pg = PuzzleGenerator()
    tracker = PerformanceTracker(user=name)
    engine = AdaptiveEngine(initial_level=initial)

    print(f"\nHi {name}! Starting session at {initial} difficulty. {rounds} puzzles.\n")

    for i in range(1, rounds + 1):
        level = engine.current_level
        puzzle = pg.generate(level)
        print(f"Puzzle {i} — Difficulty: {level}")
        print("  ", puzzle.prompt)

        start = time.time()
        ans_raw = input("Your answer: ")
        elapsed = time.time() - start

        try:
            user_ans = float(ans_raw)
        except:
            user_ans = None

        correct = puzzle.check_answer(user_ans)
        tracker.log_attempt(puzzle, correct, elapsed, level)

        if correct:
            print(f"✅ Correct! (took {elapsed:.2f}s)\n")
        else:
            print(f"❌ Incorrect. Correct answer: {puzzle.answer} (took {elapsed:.2f}s)\n")

        engine.update(correct=correct, response_time=elapsed)

    print("\n=== Session Finished ===\n")
    total, correct, avg_time = tracker.summary()
    print(f"Total puzzles: {total}")
    print(f"Correct answers: {correct}")
    print(f"Average time per puzzle: {avg_time:.2f}s")


if __name__ == "__main__":
    main()
