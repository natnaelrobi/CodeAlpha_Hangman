import os
import random
import streamlit as st

st.set_page_config(page_title="Hangman Pro", page_icon="🎯", layout="wide")

HANGMAN_PICS = [
    """
  +---+
      |
      |
      |
     ===""",
    """
  +---+
  O   |
      |
      |
     ===""",
    """
  +---+
  O   |
  |   |
      |
     ===""",
    """
  +---+
  O   |
 /|   |
      |
     ===""",
    """
  +---+
  O   |
 /|\\  |
      |
     ===""",
    """
  +---+
  O   |
 /|\\  |
 /    |
     ===""",
    """
  +---+
  O   |
 /|\\  |
 / \\  |
     ===""",
]

WORDS = [
    "PYTHON",
    "DEVELOPER",
    "INTERNSHIP",
    "ALGORITHM",
    "PROGRAMMING",
    "INTERFACE",
    "DEPLOYMENT",
]

if "word" not in st.session_state:
  st.session_state.word = random.choice(WORDS)
  st.session_state.guessed = set()
  st.session_state.misses = 0
  st.session_state.game_over = False
  st.session_state.won = False

st.title("🎯 CodeAlpha Hangman Pro Edition")

if os.path.exists("banner.jpg"):
  st.image("banner.jpg", use_container_width=True)

col1, col2 = st.columns([1, 2])

with col1:
  st.markdown(f"```text\n{HANGMAN_PICS[st.session_state.misses]}\n```")

with col2:
  display_word = " ".join([
      char if char in st.session_state.guessed else "_"
      for char in st.session_state.word
  ])
  st.markdown(
      f"<h1 style='text-align: center; letter-spacing: 5px; font-size:"
      f" 3rem;'>{display_word}</h1>",
      unsafe_allow_html=True,
  )
  st.write("")
  st.write("")

  if not st.session_state.game_over:
    cols = st.columns(7)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for i, letter in enumerate(alphabet):
      if cols[i % 7].button(
          letter,
          key=letter,
          use_container_width=True,
          disabled=letter in st.session_state.guessed,
      ):
        st.session_state.guessed.add(letter)
        if letter not in st.session_state.word:
          st.session_state.misses += 1

        if st.session_state.misses == len(HANGMAN_PICS) - 1:
          st.session_state.game_over = True
          st.session_state.won = False
        elif all(c in st.session_state.guessed for c in st.session_state.word):
          st.session_state.game_over = True
          st.session_state.won = True

        st.rerun()

if st.session_state.game_over:
  st.markdown("---")
  if st.session_state.won:
    st.success(f"🎉 INCREDIBLE! You guessed the word: {st.session_state.word}")
    st.balloons()

    if os.path.exists("win_effect.mp3"):
      st.audio("win_effect.mp3", autoplay=True)
    if os.path.exists("victory.mp4"):
      st.video("victory.mp4")

  else:
    st.error(f"💥 GAME OVER! The correct word was: {st.session_state.word}")

    if os.path.exists("lose_effect.mp3"):
      st.audio("lose_effect.mp3", autoplay=True)

  if st.button("🔄 Play Again", use_container_width=True):
    for key in list(st.session_state.keys()):
      del st.session_state[key]
    st.rerun()
