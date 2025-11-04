import random
from dataclasses import dataclass
from typing import Callable, Tuple

@dataclass
class Puzzle:
    prompt: str
    answer: float
    meta: dict

    def check_answer(self, user_answer):
        if user_answer is None:
            return False
        try:
            return abs(float(user_answer) - float(self.answer)) < 1e-6
        except:
            return False


class PuzzleGenerator:
    def __init__(self):
        pass

    def generate(self, difficulty: str) -> Puzzle:
        if difficulty == "Easy":
            return self._easy()
        elif difficulty == "Medium":
            return self._medium()
        elif difficulty == "Hard":
            return self._hard()
        else:
            raise ValueError("Invalid difficulty level!")

    def _easy(self) -> Puzzle:
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        op = random.choice(['+', '-'])
        prompt = f"{a} {op} {b} = ?"
        answer = a + b if op == "+" else a - b
        return Puzzle(prompt, answer, {"a": a, "b": b, "op": op})

    def _medium(self) -> Puzzle:
        choice = random.random()
        if choice < 0.5:
            a = random.randint(10, 99)
            b = random.randint(1, 99)
            op = random.choice(["+", "-"])
            prompt = f"{a} {op} {b} = ?"
            answer = a + b if op == "+" else a - b
        else:
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            prompt = f"{a} * {b} = ?"
            answer = a * b
        return Puzzle(prompt, answer, {"op": "mix", "choice": choice})

    def _hard(self) -> Puzzle:
        choice = random.random()
        if choice < 0.6:
            a = random.randint(10, 99)
            b = random.randint(2, 20)
            prompt = f"{a} * {b} = ?"
            answer = a * b
        else:
            b = random.randint(2, 12)
            q = random.randint(2, 12)
            a = b * q
            prompt = f"{a} / {b} = ?"
            answer = q
        return Puzzle(prompt, answer, {"op": "hard", "choice": choice})


# ✅ Interactive loop
if __name__ == "__main__":
    gen = PuzzleGenerator()
    print("🎮 Welcome to the Puzzle Game!")
    print("Type 'exit' anytime to quit.\n")

    while True:
        level = input("Choose difficulty (Easy / Medium / Hard): ").capitalize()
        if level.lower() == "exit":
            print("👋 Thanks for playing!")
            break

        try:
            puzzle = gen.generate(level)
        except ValueError:
            print("❌ Invalid choice! Please enter Easy, Medium, or Hard.\n")
            continue

        print("\nSolve this puzzle:")
        print(puzzle.prompt)
        user_input = input("Your answer (or type 'exit' to quit): ")

        if user_input.lower() == "exit":
            print("👋 Thanks for playing!")
            break

        if puzzle.check_answer(user_input):
            print("✅ Correct!\n")
        else:
            print(f"❌ Wrong! The correct answer was: {puzzle.answer}\n")
