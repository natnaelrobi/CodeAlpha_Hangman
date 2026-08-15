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


def find_file(filename):
  if os.path.exists(filename):
    return filename
  alt_path = os.path.join("CodeAlpha_Hangman", filename)
  if os.path.exists(alt_path):
    return alt_path
  return filename


if "word" not in st.session_state:
  st.session_state.word = random.choice(WORDS)
  st.session_state.guessed = set()
  st.session_state.misses = 0
  st.session_state.game_over = False
  st.session_state.won = False

st.title("🎯 CodeAlpha Hangman Pro Edition")

banner_file = find_file("banner.jpg")
if os.path.exists(banner_file):
  st.image(banner_file, use_container_width=True)

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

    win_audio = find_file("win_effect.mp3")
    if os.path.exists(win_audio):
      st.audio(win_audio, autoplay=True)

    victory_video = find_file("victory.mp4")
    if os.path.exists(victory_video):
      st.video(victory_video)

  else:
    st.error(f"💥 GAME OVER! The correct word was: {st.session_state.word}")

    lose_audio = find_file("lose_effect.mp3")
    if os.path.exists(lose_audio):
      st.audio(lose_audio, autoplay=True)

  if st.button("🔄 Play Again", use_container_width=True):
    for key in list(st.session_state.keys()):
      del st.session_state[key]
    st.rerun()
