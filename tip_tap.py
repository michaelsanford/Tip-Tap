#!/usr/bin/env python3
"""A typing game for youngsters."""

import tkinter as tk
import random
import argparse

JOYFUL_RESPONSES = [
    "🎉 Excellent! 🎉",
    "⭐ Amazing! ⭐",
    "🌟 Perfect! 🌟",
    "🎊 Wonderful! 🎊",
    "✨ Great job! ✨",
    "🏆 Fantastic! 🏆",
    "🎈 Well done! 🎈",
    "🌈 Brilliant! 🌈"
]

COLORS = ['#00FF41', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']


class TypingGame:
    """Main typing game class."""

    def __init__(self, use_letters=True, use_numbers=False):
        """Initialize the typing game."""
        self.score = 0
        self.color_index = 0
        self.target_letter = None
        self.character_set = []
        if use_letters:
            self.character_set.extend('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        if use_numbers:
            self.character_set.extend('0123456789')
        self.root = tk.Tk()
        self.root.title("Tip-Tap Typing Game")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<Configure>', self.on_resize)
        self.root.focus_set()

        # Create main frame that centers content
        self.main_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.score_label = tk.Label(self.main_frame, text=f"Score: {self.score}",
                                   font=('Arial', 20, 'bold'), fg='#00d4ff', bg='#1a1a2e')
        self.score_label.pack(pady=20)

        # Container for letter with shadow effect
        self.letter_frame = tk.Frame(self.main_frame, bg='#1a1a2e')
        self.letter_frame.pack(pady=40)
        
        self.shadow_label = tk.Label(self.letter_frame, text="",
                                    font=('Arial', 200, 'bold'), fg='#333333', bg='#1a1a2e')
        self.shadow_label.place(x=2, y=2)
        
        self.letter_label = tk.Label(self.letter_frame, text="",
                                    font=('Arial', 200, 'bold'), fg='#00FF41', bg='#1a1a2e')
        self.letter_label.pack()

        self.prompt_label = tk.Label(self.main_frame, text="Press any key to start!",
                                    font=('Arial', 18), fg='#00d4ff', bg='#1a1a2e')
        self.prompt_label.pack(pady=20)

        self.response_label = tk.Label(self.main_frame, text="",
                                      font=('Arial', 16, 'bold'), fg='#00ff88', bg='#1a1a2e')
        self.response_label.pack(pady=15)

        self.new_round()

    def new_round(self):
        """Start a new round with a random character."""
        self.target_letter = random.choice(self.character_set)
        
        # Cycle through colors
        current_color = COLORS[self.color_index]
        self.color_index = (self.color_index + 1) % len(COLORS)

        # Update both shadow and main letter
        self.shadow_label.config(text=self.target_letter)
        self.letter_label.config(text=self.target_letter, fg=current_color)
        self.prompt_label.config(text=f"Press the '{self.target_letter}' key!")
        self.response_label.config(text="")

    def flash_screen(self):
        """Flash the screen with a success effect."""
        # Create a bright flash effect
        self.root.configure(bg='#00ff88')
        self.main_frame.configure(bg='#00ff88')
        self.root.after(100, self.restore_colors)
        
    def restore_colors(self):
        """Restore original colors after flash."""
        self.root.configure(bg='#1a1a2e')
        self.main_frame.configure(bg='#1a1a2e')

    def on_resize(self, event):
        """Scale letter font based on window size."""
        if event.widget == self.root:
            font_size = min(self.root.winfo_width(), self.root.winfo_height()) // 4
            font_size = max(50, min(font_size, 300))  # Keep between 50-300
            self.letter_label.config(font=('Arial', font_size, 'bold'))
            self.shadow_label.config(font=('Arial', font_size, 'bold'))

    def on_key_press(self, event):
        """Handle key press events."""
        pressed_key = event.char.upper()

        if pressed_key == self.target_letter:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            response = random.choice(JOYFUL_RESPONSES)
            self.response_label.config(text=response, fg='#00ff88')
            self.root.bell()
            self.flash_screen()
            self.root.after(1200, self.new_round)
        elif pressed_key.isalnum():
            error_msg = f"Oops! You pressed '{pressed_key}', try '{self.target_letter}'"
            self.response_label.config(text=error_msg, fg='#ff4757')

    def run(self):
        """Start the game main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A typing game for youngsters')
    parser.add_argument('-letters', action='store_true', help='Enable letters (A-Z)')
    parser.add_argument('-numbers', action='store_true', help='Enable numbers (0-9)')
    args = parser.parse_args()
    
    # Default to letters if no flags specified
    use_letters = args.letters or not (args.letters or args.numbers)
    use_numbers = args.numbers
    
    game = TypingGame(use_letters, use_numbers)
    game.run()
