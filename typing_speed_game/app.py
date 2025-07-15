import streamlit as st
import time
import random
import csv
from datetime import datetime
import os

st.set_page_config(page_title="⌨️ Typing Speed Game", layout="centered")
st.title("⌨️ Typing Speed Game with Scoreboard")

sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Streamlit makes Python apps easy to build.",
    "Typing fast takes practice and accuracy.",
    "Jay is building awesome Python projects.",
    "Always test your code before you push it."
]

SCOREBOARD_FILE = "scoreboard.csv"

if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "target_sentence" not in st.session_state:
    st.session_state.target_sentence = random.choice(sentences)

if not st.session_state.game_started:
    if st.button("🚀 Start Typing Test"):
        st.session_state.target_sentence = random.choice(sentences)
        st.session_state.start_time = time.time()
        st.session_state.game_started = True

if st.session_state.game_started:
    st.markdown(f"**Type this sentence:**")
    st.code(st.session_state.target_sentence)
    user_input = st.text_area("Start typing here...", height=100)
    st.session_state.user_text = user_input

    if st.button("✅ Submit"):
        end_time = time.time()
        time_taken = round(end_time - st.session_state.start_time, 2)
        words = len(st.session_state.target_sentence.split())
        wpm = round((words / time_taken) * 60, 2)

        accuracy = sum(1 for i, c in enumerate(user_input) if i < len(st.session_state.target_sentence) and c == st.session_state.target_sentence[i])
        accuracy = round((accuracy / len(st.session_state.target_sentence)) * 100, 2)

        st.success(f"⏱ Time: {time_taken} seconds | 💬 WPM: {wpm} | 🎯 Accuracy: {accuracy}%")

        name = st.text_input("Enter your name for the scoreboard:")
        if st.button("🏁 Save to Scoreboard") and name:
            with open(SCOREBOARD_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([name, wpm, accuracy, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            st.success("🎉 Score saved!")
            st.session_state.game_started = False

st.markdown("---")
st.subheader("🏆 Leaderboard")
if os.path.exists(SCOREBOARD_FILE):
    with open(SCOREBOARD_FILE, newline="") as f:
        reader = csv.reader(f)
        scores = sorted(reader, key=lambda row: float(row[1]), reverse=True)[:5]
        for row in scores:
            st.write(f"👤 {row[0]} | 💬 WPM: {row[1]} | 🎯 Accuracy: {row[2]}% | 🕓 {row[3]}")
else:
    st.info("No scores yet. Be the first to play!")