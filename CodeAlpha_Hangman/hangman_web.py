import os
import random
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Hangman Pro - CodeAlpha", page_icon="🎮", layout="centered"
)

# Display Banner Image
banner_path = "CodeAlpha_Hangman/banner.jpg"
if os.path.exists(banner_path):
  st.image(banner_path, use_column_width=True)

st.title("🎯 CodeAlpha Hangman Game")
st.write("Guess the secret word letter by letter before you run out of lives!")

# Word list
WORDS = [
    "PYTHON",
    "STREAMLIT",
    "PROGRAMMING",
    "DEVELOPER",
    "INTERNSHIP",
    "CODEALPHA",
    "ALGORITHM",
]

# Initialize session state
if "word" not in st.session_state:
  st.session_state.word = random.choice(WORDS)
  st.session_state.guessed_letters = set()
  st.session_state.attempts_left = 6
  st.session_state.game_over = False
  st.session_state.won = False


def reset_game():
  st.session_state.word = random.choice(WORDS)
  st.session_state.guessed_letters = set()
  st.session_state.attempts_left = 6
  st.session_state.game_over = False
  st.session_state.won = False


# Display current word status
word_display = "".join(
    [
        letter if letter in st.session_state.guessed_letters else "_"
        for letter in st.session_state.word
    ]
)

st.markdown(f"### Word: `{word_display}`")
st.write(f"❤️ Lives remaining: {st.session_state.attempts_left}")
st.write(
    f"❌ Guessed letters:"
    f" {', '.join(sorted(st.session_state.guessed_letters)) if st.session_state.guessed_letters else 'None'}"
)

# Game logic & input
if not st.session_state.game_over:
  with st.form("guess_form", clear_on_submit=True):
    guess = st.text_input("Enter a letter:", max_chars=1).upper()
    submitted = st.form_submit_button("Guess")

    if submitted and guess:
      if not guess.isalpha():
        st.warning("Please enter a valid alphabetic letter.")
      elif guess in st.session_state.guessed_letters:
        st.info(f"You already guessed '{guess}'. Try another one.")
      else:
        st.session_state.guessed_letters.add(guess)
        if guess in st.session_state.word:
          st.success(f"Good job! '{guess}' is in the word.")
        else:
          st.session_state.attempts_left -= 1
          st.error(f"Incorrect! '{guess}' is not in the word.")

        # Check win condition
        if all(
            letter in st.session_state.guessed_letters
            for letter in st.session_state.word
        ):
          st.session_state.game_over = True
          st.session_state.won = True

        # Check lose condition
        elif st.session_state.attempts_left <= 0:
          st.session_state.game_over = True
          st.session_state.won = False

        st.rerun()

# Game Over State (Win / Lose)
if st.session_state.game_over:
  if st.session_state.won:
    st.balloons()
    st.success(
        f"🎉 Congratulations! You guessed the word: {st.session_state.word}"
    )

    win_audio = "CodeAlpha_Hangman/win_effect.mp3"
    if os.path.exists(win_audio):
      st.audio(win_audio, format="audio/mp3")

    victory_video = "CodeAlpha_Hangman/victory.mp4"
    if os.path.exists(victory_video):
      st.video(victory_video)

  else:
    st.error(f"💀 Game Over! The secret word was: {st.session_state.word}")

    lose_audio = "CodeAlpha_Hangman/lose_effect.mp3"
    if os.path.exists(lose_audio):
      st.audio(lose_audio, format="audio/mp3")

  if st.button("Play Again"):
    reset_game()
    st.rerun()
