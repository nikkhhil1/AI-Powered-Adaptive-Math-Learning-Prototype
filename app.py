import streamlit as st
import time
import pandas as pd
from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine_ml import AdaptiveEngineML
from progress_summary import ProgressSummary

st.set_page_config(page_title="AI-Powered Adaptive Math Learning", page_icon="🧠")

# --- App State ---
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.tracker = None
    st.session_state.engine = None
    st.session_state.puzzle = None
    st.session_state.pg = None
    st.session_state.last_time = None
    st.session_state.round = 1

# --- Header ---
st.title("🧠 AI-Powered Adaptive Math Learning Prototype")
st.markdown("Practice math problems with adaptive difficulty that adjusts to your skill level!")

# --- Start Screen ---
if not st.session_state.started:
    name = st.text_input("Enter your name:", "")
    diff = st.selectbox("Choose initial difficulty:", ["Easy", "Medium", "Hard"])
    total = st.number_input("Number of puzzles:", min_value=3, max_value=30, value=10)
    start_btn = st.button("🚀 Start Session")

    if start_btn and name.strip():
        st.session_state.name = name.strip()
        st.session_state.rounds = total
        st.session_state.pg = PuzzleGenerator()
        st.session_state.tracker = PerformanceTracker(user=name)
        st.session_state.engine = AdaptiveEngineML(initial_level=diff)
        st.session_state.started = True
        st.session_state.round = 1
        st.session_state.puzzle = st.session_state.pg.generate(diff)
        st.session_state.last_time = time.time()
        st.rerun()

else:
    # --- Active Session ---
    total_rounds = st.session_state.rounds
    current_round = st.session_state.round
    engine = st.session_state.engine
    tracker = st.session_state.tracker
    puzzle = st.session_state.puzzle
    pg = st.session_state.pg

    st.subheader(f"Round {current_round}/{total_rounds}")
    st.markdown(f"*Difficulty:* {engine.current_level}")
    st.markdown(f"### ❓ {puzzle.prompt}")

    user_answer = st.text_input("Your answer:", key=f"answer_{current_round}")
    submit_btn = st.button("Submit")

    if submit_btn:
        elapsed = time.time() - st.session_state.last_time
        try:
            ans = float(user_answer)
        except:
            ans = None

        correct = puzzle.check_answer(ans)
        tracker.log_attempt(puzzle, correct, elapsed, engine.current_level)

        if correct:
            st.success(f"✅ Correct! (took {elapsed:.2f}s)")
        else:
            st.error(f"❌ Incorrect. Correct answer was {puzzle.answer} (took {elapsed:.2f}s)")

        next_level = engine.update(correct=correct, response_time=elapsed)
        st.session_state.round += 1

        if st.session_state.round <= total_rounds:
            st.session_state.puzzle = pg.generate(next_level)
            st.session_state.last_time = time.time()
            st.rerun()
        else:
            st.session_state.started = False

            st.success("🎉 Session Complete!")
            summary = ProgressSummary(tracker)
            df = tracker.to_dataframe()

            st.subheader("📊 Performance Summary")
            total = len(df)
            acc = df["correct"].mean() * 100
            avg_time = df["time_taken"].mean()
            st.write(f"*Accuracy:* {acc:.1f}%  |  *Avg Time:* {avg_time:.2f}s")

            st.dataframe(df[["difficulty", "prompt", "correct", "time_taken"]].tail(10))
            summary.print_summary()
            csv_path = tracker.save_csv()
            st.info(f"Session log saved to {csv_path}")

            if st.button("🔁 Restart"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()