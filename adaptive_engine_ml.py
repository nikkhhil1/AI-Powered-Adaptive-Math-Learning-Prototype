"""
ML-based Adaptive Engine.

- Uses DecisionTreeClassifier to predict next difficulty (Easy/Medium/Hard)
  given recent performance features.
- If no saved model exists, generates simulated training data using
  heuristics, trains a decision tree, and saves it.
- Keeps a small rolling buffer of real attempts; retrains the model
  when enough new real data points are collected (configurable).
"""

import os
import joblib
import numpy as np
import random
from collections import deque
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

MODEL_PATH = "model_adaptive_dt.joblib"

LEVELS = ["Easy", "Medium", "Hard"]
LEVEL_TO_INT = {l: i for i, l in enumerate(LEVELS)}
INT_TO_LEVEL = {i: l for l, i in LEVEL_TO_INT.items()}


def _heuristic_label(cur_level_int, correct_count, avg_time):
    """Heuristic to generate label for simulated training data."""
    time_thresh = [8.0, 12.0, 18.0]  # for Easy/Medium/Hard
    if correct_count >= 2 and avg_time <= time_thresh[cur_level_int]:
        return min(cur_level_int + 1, 2)
    if correct_count <= 1 or avg_time > time_thresh[cur_level_int] * 1.5:
        return max(cur_level_int - 1, 0)
    return cur_level_int


def generate_simulated_data(n_samples=2000, window=3, seed=42):
    """Simulate dataset for training."""
    random.seed(seed)
    np.random.seed(seed)
    X, y = [], []
    for _ in range(n_samples):
        cur_level = random.choice([0, 1, 2])
        corrects = [random.random() < (0.6 + 0.1 * (cur_level - 1)) for _ in range(window)]
        correct_count = sum(1 for c in corrects if c)
        base = [6, 10, 16][cur_level]
        avg_time = max(1.0, random.gauss(base, base * 0.3))
        last_correct = 1 if corrects[-1] else 0
        label = _heuristic_label(cur_level, correct_count, avg_time)
        X.append([cur_level, correct_count, avg_time, last_correct])
        y.append(label)
    return np.array(X), np.array(y)


class AdaptiveEngineML:
    def __init__(self, initial_level="Easy", model_path=MODEL_PATH,
                 window=3, retrain_after=30, random_state=42):  # ✅ FIXED HERE
        self.window = window
        self.retrain_after = retrain_after
        self.history = deque(maxlen=self.window)
        self.current_level = initial_level if initial_level in LEVELS else "Easy"
        self.model_path = model_path
        self.random_state = random_state

        self.new_examples_X = []
        self.new_examples_y = []

        if os.path.exists(self.model_path):
            self.clf = joblib.load(self.model_path)
            print(f"✅ Loaded model from {self.model_path}")
        else:
            print("⚙️ No saved ML model found — training initial model from simulated data...")
            X, y = generate_simulated_data(n_samples=2500, window=self.window, seed=self.random_state)
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=self.random_state)
            clf = DecisionTreeClassifier(max_depth=6, random_state=self.random_state)
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_val)
            print(f"Initial simulated model accuracy (val): {accuracy_score(y_val, y_pred):.3f}")
            self.clf = clf
            joblib.dump(self.clf, self.model_path)
            print(f"💾 Saved initial model to {self.model_path}")

    def _features_from_history(self, cur_level_int):
        """Build feature vector from history."""
        hist = list(self.history)
        if not hist:
            return np.array([cur_level_int, 1, 10.0, 1]).reshape(1, -1)
        correct_count = sum(1 for c, t in hist if c)
        avg_time = sum(t for c, t in hist) / len(hist)
        last_correct = 1 if hist[-1][0] else 0
        return np.array([cur_level_int, correct_count, avg_time, last_correct]).reshape(1, -1)

    def predict_next_level(self):
        cur_idx = LEVEL_TO_INT[self.current_level]
        X = self._features_from_history(cur_idx)
        pred_int = int(self.clf.predict(X)[0])
        return INT_TO_LEVEL.get(pred_int, self.current_level)

    def update(self, correct: bool, response_time: float):
        """Update after each attempt."""
        self.history.append((correct, response_time))
        cur_idx = LEVEL_TO_INT[self.current_level]
        correct_count = sum(1 for c, t in self.history if c)
        avg_time = sum(t for c, t in self.history) / len(self.history)
        last_correct = 1 if self.history[-1][0] else 0
        feat = [cur_idx, correct_count, avg_time, last_correct]
        label = _heuristic_label(cur_idx, correct_count, avg_time)
        self.new_examples_X.append(feat)
        self.new_examples_y.append(label)

        if len(self.new_examples_y) >= self.retrain_after:
            print("🔁 Retraining adaptive model with new data...")
            try:
                X_sim, y_sim = generate_simulated_data(n_samples=2000, window=self.window, seed=self.random_state + 1)
                X_comb = np.vstack([X_sim, np.array(self.new_examples_X)])
                y_comb = np.concatenate([y_sim, np.array(self.new_examples_y)])
                clf = DecisionTreeClassifier(max_depth=6, random_state=self.random_state)
                clf.fit(X_comb, y_comb)
                self.clf = clf
                joblib.dump(self.clf, self.model_path)
                print(f"✅ Model retrained and saved at {self.model_path}")
            except Exception as e:
                print("❌ Retrain failed:", e)
            self.new_examples_X = []
            self.new_examples_y = []

        next_level = self.predict_next_level()
        cur_idx = LEVEL_TO_INT[self.current_level]
        next_idx = LEVEL_TO_INT[next_level]
        if next_idx > cur_idx:
            self.current_level = LEVELS[min(cur_idx + 1, 2)]
        elif next_idx < cur_idx:
            self.current_level = LEVELS[max(cur_idx - 1, 0)]
        else:
            self.current_level = LEVELS[cur_idx]
        return self.current_level

if __name__ == "__main__":
    engine = AdaptiveEngineML()
    for i in range(5):
        correct = random.choice([True, False])
        time = random.uniform(5, 20)
        level = engine.update(correct, time)
        print(f"Attempt {i+1}: correct={correct}, time={time:.1f}s → Next level: {level}")
