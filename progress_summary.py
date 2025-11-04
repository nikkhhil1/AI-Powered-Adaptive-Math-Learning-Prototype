import pandas as pd
import numpy as np

class ProgressSummary:
    def __init__(self, tracker):
        self.tracker = tracker

    def show_summary(self):
        print("Progress summary:", self.tracker.get_summary())


    def print_summary(self):
        df = self.tracker.to_dataframe()
        if df.empty:
            print("No attempts recorded.")
            return

        total = len(df)
        correct = int(df['correct'].sum())
        accuracy = correct / total * 100.0
        avg_time = df['time_taken'].mean()
        by_diff = df.groupby('difficulty').agg(
            attempts=('prompt','count'),
            accuracy=('correct', lambda x: x.mean() * 100),
            avg_time=('time_taken','mean')
        ).reset_index()

        print(f"Total attempts: {total}")
        print(f"Correct: {correct} | Accuracy: {accuracy:.1f}%")
        print(f"Average response time: {avg_time:.2f} s")
        print("\nPerformance by difficulty:")
        print(by_diff.to_string(index=False, float_format='{:,.2f}'.format))

        # trend (last 5)
        last_n = df.tail(5)
        if not last_n.empty:
            trend_acc = last_n['correct'].mean() * 100
            trend_time = last_n['time_taken'].mean()
            print(f"\nRecent trend (last {len(last_n)}): Accuracy {trend_acc:.1f}%, Avg time {trend_time:.2f}s")

        # recommended next level heuristic
        # If recent performance strong -> recommend increase, if weak -> decrease else same
        rec = self._recommend_next_level(df)
        print(f"\nRecommended next level: {rec}")

    def _recommend_next_level(self, df):
        # use last 3 attempts
        last = df.tail(3)
        if last.empty:
            return "Medium"
        acc = last['correct'].mean()
        time_avg = last['time_taken'].mean()
        # simple heuristic:
        if acc >= 0.66 and time_avg < 12:
            # increase if possible
            # derive most recent difficulty
            most_recent = last.iloc[-1]['difficulty']
            order = ["Easy","Medium","Hard"]
            idx = order.index(most_recent)
            return order[min(idx+1, 2)]
        if acc <= 0.33 or time_avg > 18:
            most_recent = last.iloc[-1]['difficulty']
            order = ["Easy","Medium","Hard"]
            idx = order.index(most_recent)
            return order[max(idx-1, 0)]
        return last.iloc[-1]['difficulty']