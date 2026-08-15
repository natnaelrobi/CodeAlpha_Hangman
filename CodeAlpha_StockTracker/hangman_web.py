import tkinter as tk
from tkinter import messagebox
import random

HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\\  |
      |
     ===''', '''
  +---+
  O   |
 /|\\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\\  |
 / \\  |
     ===''']

WORDS = ["PYTHON", "DEVELOPER", "INTERNSHIP", "ALGORITHM", "PROGRAMMING"]

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeAlpha - Hangman")
        self.root.geometry("400x450")
        
        self.word = random.choice(WORDS)
        self.correct = ""
        self.missed = ""
        
        self.art_label = tk.Label(root, text=HANGMAN_PICS[0], font=("Courier", 14), justify=tk.LEFT)
        self.art_label.pack(pady=10)
        
        self.word_label = tk.Label(root, text="_ " * len(self.word), font=("Arial", 20, "bold"))
        self.word_label.pack(pady=15)
        
        self.entry = tk.Entry(root, font=("Arial", 14), width=5, justify="center")
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.guess)
        
        self.btn = tk.Button(root, text="Guess Letter", command=self.guess, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.btn.pack()

    def guess(self, event=None):
        g = self.entry.get().upper().strip()
        self.entry.delete(0, tk.END)
        
        if len(g) != 1 or not g.isalpha() or g in self.correct + self.missed:
            return
            
        if g in self.word:
            self.correct += g
        else:
            self.missed += g
            
        self.update_ui()

    def update_ui(self):
        self.art_label.config(text=HANGMAN_PICS[len(self.missed)])
        display = [c if c in self.correct else "_" for c in self.word]
        self.word_label.config(text=" ".join(display))
        
        if "_" not in display:
            messagebox.showinfo("Hangman", f"🎉 You Win! The word was {self.word}")
            self.reset()
        elif len(self.missed) == len(HANGMAN_PICS) - 1:
            messagebox.showerror("Hangman", f"💥 Game Over! The word was {self.word}")
            self.reset()

    def reset(self):
        self.word = random.choice(WORDS)
        self.correct = ""
        self.missed = ""
        self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()