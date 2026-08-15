# Snake Game for Code in Place IDE
# FIXED VERSION: Uses Python's Built-in Native Tkinter Canvas Engine

import tkinter as tk
import random
import time

# --- GAME SETTINGS ---
GRID_SIZE = 20
CELL_SIZE = 25
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
MOVE_DELAY = 0.15


class SnakeGame:
    def __init__(self):
        # Create native window and canvas object
        self.root = tk.Tk()
        self.root.title("🐍 SPEED DEMON SNAKE 🐍")
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="white", highlightthickness=0)
        self.canvas.pack()

        # State variables
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = "right"
        self.next_direction = "right"
        self.food = None
        self.food_object = None
        self.bad_food = None
        self.bad_food_object = None
        self.bad_food_text = None
        self.score = 0
        self.high_score = 0
        self.delay = MOVE_DELAY
        self.game_active = False
        self.snake_objects = []
        self.game_over_objects = []

        # Bind Key events natively
        self.root.bind("<Key>", self.handle_input)

        # Show start screen
        self.show_start_screen()

        self.score_text = None

    def start_new_game(self):
        """Resets the game state for a new round."""
        self.canvas.delete("all")
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = "right"
        self.next_direction = "right"
        self.score = 0
        self.delay = MOVE_DELAY
        self.game_active = True
        self.snake_objects.clear()
        self.game_over_objects.clear()

        self.score_text = self.canvas.create_text(80, 20,
                                                  text=f"Score: 0  High: {self.high_score}",
                                                  font=("Arial", 18),
                                                  fill="black")
        self.spawn_food()

    def show_start_screen(self):
        """Display start screen with game instructions."""
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="white")

        # Decorative borders
        self.canvas.create_rectangle(10, 10, WIDTH - 10, HEIGHT - 10, outline="#2ecc71", width=2)
        self.canvas.create_rectangle(14, 14, WIDTH - 14, HEIGHT - 14, outline="#27ae60", width=2)

        # Title
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 140, text="🐍 SPEED DEMON SNAKE 🐍", font=("Arial", 26, "bold"),
                                fill="#2c3e50")
        self.canvas.create_line(WIDTH // 2 - 150, HEIGHT // 2 - 100, WIDTH // 2 + 150, HEIGHT // 2 - 100,
                                fill="#bdc3c7")

        # Controls & Rules
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 65, text="🎮 CONTROLS", font=("Arial", 18, "bold"),
                                fill="#2980b9")
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 30, text="Use ARROW KEYS ( ↑ ↓ ← → ) to move",
                                font=("Arial", 16), fill="#2c3e50")
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 20, text="📋 RULES", font=("Arial", 18, "bold"),
                                fill="#2980b9")
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 50, text="🍎 Red Apple: +10 points", font=("Arial", 14),
                                fill="#2c3e50")
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 75, text="☠️ Purple Skull: +50 points! (High reward!)",
                                font=("Arial", 14), fill="#2c3e50")
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 100, text="⚡ Speed increases every 50 points!",
                                font=("Arial", 14), fill="#2c3e50")
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 155, text="👉 Press SPACE to start! 👈",
                                font=("Arial", 20, "bold"), fill="#e74c3c")
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 200, text="🏆 Try to get the highest score!",
                                font=("Arial", 14), fill="#7f8c8d")

    def draw_rect(self, x, y, fill_color, outline_color="black"):
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        return self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=outline_color)

    def spawn_food(self):
        if self.food_object: self.canvas.delete(self.food_object)
        if self.bad_food_object: self.canvas.delete(self.bad_food_object)
        if self.bad_food_text: self.canvas.delete(self.bad_food_text)

        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

        if self.score >= 50 and random.random() < 0.30:
            while True:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                if (x, y) not in self.snake and (x, y) != self.food:
                    self.bad_food = (x, y)
                    break
        else:
            self.bad_food = None

        if self.food:
            self.food_object = self.draw_rect(self.food[0], self.food[1], "red", "yellow")
        if self.bad_food:
            self.bad_food_object = self.draw_rect(self.bad_food[0], self.bad_food[1], "purple", "black")
            x1 = self.bad_food[0] * CELL_SIZE + CELL_SIZE // 2
            y1 = self.bad_food[1] * CELL_SIZE + CELL_SIZE // 2
            self.bad_food_text = self.canvas.create_text(x1, y1, text="☠", font=("Arial", 16), fill="white")

    def handle_input(self, event):
        key = event.keysym.lower()
        if key == "space" and not self.game_active:
            self.start_new_game()
            return

        # Maps keyboard keys directly
        key_map = {"up": "up", "down": "down", "left": "left", "right": "right"}
        opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}

        if key in key_map:
            new_dir = key_map[key]
            if new_dir != opposites.get(self.direction):
                self.next_direction = new_dir

    def update_snake(self):
        if not self.game_active: return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]

        if self.direction == "up":
            head_y -= 1
        elif self.direction == "down":
            head_y += 1
        elif self.direction == "left":
            head_x -= 1
        elif self.direction == "right":
            head_x += 1

        new_head = (head_x, head_y)

        if (head_x < 0 or head_x >= GRID_SIZE or head_y < 0 or head_y >= GRID_SIZE or new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
            if self.score % 50 == 0:
                self.delay = max(0.05, self.delay - 0.02)
            self.spawn_food()
        elif self.bad_food and new_head == self.bad_food:
            self.score += 50
            if self.score > self.high_score:
                self.high_score = self.score
            self.spawn_food()
        else:
            self.snake.pop()

    def render(self):
        if not self.game_active: return

        for obj in self.snake_objects:
            self.canvas.delete(obj)
        self.snake_objects.clear()

        for i, segment in enumerate(self.snake):
            fill = "#66ff66" if i == 0 else "#228b22"
            outline = "white" if i == 0 else "green"
            rect = self.draw_rect(segment[0], segment[1], fill, outline)
            self.snake_objects.append(rect)

        if self.score_text:
            self.canvas.delete(self.score_text)
        self.score_text = self.canvas.create_text(80, 20,
                                                  text=f"Score: {self.score}  High: {self.high_score}",
                                                  font=("Arial", 18),
                                                  fill="black")

    def game_over(self):
        self.game_active = False
        for obj in self.game_over_objects:
            self.canvas.delete(obj)
        self.game_over_objects.clear()

        if self.bad_food_text: self.canvas.delete(self.bad_food_text)

        obj1 = self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 60, text="💀 GAME OVER 💀", font=("Arial", 36),
                                       fill="red")
        obj2 = self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text=f"Final Score: {self.score}", font=("Arial", 28),
                                       fill="#f39c12")
        obj3 = self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 45, text=f"High Score: {self.high_score}",
                                       font=("Arial", 24), fill="#2c3e50")
        obj4 = self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 95, text="👉 Press SPACE to try again! 👈",
                                       font=("Arial", 18, "bold"), fill="#e74c3c")

        self.game_over_objects.extend([obj1, obj2, obj3, obj4])

    def run(self):
        """Native Tkinter main loop implementation."""

        def loop():
            if self.game_active:
                self.update_snake()
                self.render()
            self.root.after(int(self.delay * 1000), loop)

        self.root.after(int(self.delay * 1000), loop)
        self.root.mainloop()


if __name__ == '__main__':
    game = SnakeGame()
    game.run()
