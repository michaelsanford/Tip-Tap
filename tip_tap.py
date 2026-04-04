#!/usr/bin/env python3
"""A typing game for youngsters."""

import tkinter as tk
import random
import argparse
import threading

try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

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

STREAK_RESPONSES = {
    3:  "🔥 3 in a row! 🔥",
    5:  "🚀 5 streak! 🚀",
    10: "👑 10 STREAK!! 👑",
}

COLORS = ['#00FF41', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
RAINBOW = ['#FF0000', '#FF7700', '#FFFF00', '#00FF00', '#0088FF', '#8800FF', '#FF00AA']
CONFETTI_COLORS = ['#FF6B6B', '#FFE66D', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD',
                   '#FF9FF3', '#54A0FF', '#5F27CD', '#00D2D3', '#FF9F43', '#1DD1A1']
POP_FRACS = [0.15, 0.55, 1.08, 0.92, 1.03, 1.0]
SHAKE_OFFSETS = [14, -14, 10, -10, 6, -6, 0]  # absolute x deltas from centre


def _play_success():
    if HAS_SOUND:
        for freq, dur in [(523, 80), (659, 80), (784, 140)]:
            winsound.Beep(freq, dur)


def _play_error():
    if HAS_SOUND:
        for freq, dur in [(280, 90), (220, 130)]:
            winsound.Beep(freq, dur)


class TypingGame:
    """Main typing game class."""

    def __init__(self, use_letters=True, use_numbers=False):
        self.score = 0
        self.streak = 0
        self.color_index = 0
        self.target_letter = None
        self.current_color = COLORS[0]
        self.letter_size = 200
        self.accepting_input = True

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

        # Grid: labels at top/bottom, letter canvas fills the middle
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)  # letter row expands

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}",
                                    font=('Arial', 20, 'bold'), fg='#00d4ff', bg='#1a1a2e')
        self.score_label.grid(row=0, column=0, pady=(20, 2))

        self.streak_label = tk.Label(self.root, text="",
                                     font=('Arial', 14, 'bold'), fg='#FF9F43', bg='#1a1a2e')
        self.streak_label.grid(row=1, column=0, pady=(0, 6))

        # Single canvas: letter + confetti all live here
        self.letter_canvas = tk.Canvas(self.root, bg='#1a1a2e', highlightthickness=0)
        self.letter_canvas.grid(row=2, column=0, sticky='nsew')

        self.prompt_label = tk.Label(self.root, text="Press any key to start!",
                                     font=('Arial', 18), fg='#00d4ff', bg='#1a1a2e')
        self.prompt_label.grid(row=3, column=0, pady=10)

        self.response_label = tk.Label(self.root, text="",
                                       font=('Arial', 16, 'bold'), fg='#00ff88', bg='#1a1a2e')
        self.response_label.grid(row=4, column=0, pady=(0, 20))

        # Letter items — positioned after window maps
        self.shadow_id = self.letter_canvas.create_text(0, 0, text="",
                                                         font=('Arial', 200, 'bold'),
                                                         fill='#2a2a4a')
        self.letter_id = self.letter_canvas.create_text(0, 0, text="",
                                                         font=('Arial', 200, 'bold'),
                                                         fill='#00FF41')

        # Defer first round until window geometry is known
        self.root.after_idle(self.new_round)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _canvas_centre(self):
        cw = self.letter_canvas.winfo_width()
        ch = self.letter_canvas.winfo_height()
        return max(cw, 1) // 2, max(ch, 1) // 2

    def _place_letter(self, dx=0):
        cx, cy = self._canvas_centre()
        self.letter_canvas.coords(self.letter_id, cx + dx, cy)
        self.letter_canvas.coords(self.shadow_id, cx + dx + 3, cy + 3)

    # ------------------------------------------------------------------
    # Game logic
    # ------------------------------------------------------------------

    def new_round(self):
        self.accepting_input = True
        self.target_letter = random.choice(self.character_set)
        self.current_color = COLORS[self.color_index]
        self.color_index = (self.color_index + 1) % len(COLORS)

        self.letter_canvas.itemconfig(self.shadow_id, text=self.target_letter)
        self.letter_canvas.itemconfig(self.letter_id,
                                       text=self.target_letter, fill=self.current_color)
        # Raise letter above any leftover confetti
        self.letter_canvas.tag_raise(self.shadow_id)
        self.letter_canvas.tag_raise(self.letter_id)

        self.prompt_label.config(text=f"Press the '{self.target_letter}' key!")
        self.response_label.config(text="")
        self._place_letter()
        self.animate_pop_in(0, self.letter_size)

    def on_key_press(self, event):
        if not self.accepting_input:
            return
        pressed_key = event.char.upper()

        if pressed_key == self.target_letter:
            self.accepting_input = False
            self.score += 1
            self.streak += 1
            self.score_label.config(text=f"Score: {self.score}")
            self._update_streak_label()

            response = STREAK_RESPONSES.get(self.streak, random.choice(JOYFUL_RESPONSES))
            self.response_label.config(text=response, fg='#00ff88')

            threading.Thread(target=_play_success, daemon=True).start()
            self.flash_screen()
            self.animate_rainbow(0)
            self.spawn_confetti()
            delay = 1800 if self.streak == 10 else 1300
            self.root.after(delay, self.new_round)

        elif pressed_key.isalnum():
            self.streak = 0
            self._update_streak_label()
            error_msg = f"Oops! You pressed '{pressed_key}', try '{self.target_letter}'"
            self.response_label.config(text=error_msg, fg='#ff4757')
            threading.Thread(target=_play_error, daemon=True).start()
            self.animate_shake(0)

    def _update_streak_label(self):
        if self.streak >= 3:
            self.streak_label.config(text=f"🔥 {self.streak}x streak!")
        else:
            self.streak_label.config(text="")

    # ------------------------------------------------------------------
    # Animations
    # ------------------------------------------------------------------

    def animate_pop_in(self, step, target_size):
        if step >= len(POP_FRACS):
            return
        size = max(20, int(target_size * POP_FRACS[step]))
        font = ('Arial', size, 'bold')
        self.letter_canvas.itemconfig(self.letter_id, font=font)
        self.letter_canvas.itemconfig(self.shadow_id, font=font)
        self.root.after(38, lambda: self.animate_pop_in(step + 1, target_size))

    def animate_shake(self, step):
        if step >= len(SHAKE_OFFSETS):
            self._place_letter()
            return
        self._place_letter(dx=SHAKE_OFFSETS[step])
        self.root.after(48, lambda: self.animate_shake(step + 1))

    def animate_rainbow(self, step):
        if step >= len(RAINBOW):
            self.letter_canvas.itemconfig(self.letter_id, fill=self.current_color)
            return
        self.letter_canvas.itemconfig(self.letter_id, fill=RAINBOW[step])
        self.root.after(52, lambda: self.animate_rainbow(step + 1))

    def flash_screen(self):
        for w in (self.root, self.score_label, self.streak_label,
                  self.prompt_label, self.response_label, self.letter_canvas):
            w.configure(bg='#00ff88')
        self.root.after(100, self.restore_colors)

    def restore_colors(self):
        for w in (self.root, self.score_label, self.streak_label,
                  self.prompt_label, self.response_label, self.letter_canvas):
            w.configure(bg='#1a1a2e')

    # ------------------------------------------------------------------
    # Confetti (drawn on the same letter_canvas, below the letter)
    # ------------------------------------------------------------------

    def spawn_confetti(self):
        self.letter_canvas.delete('confetti')
        cw = self.letter_canvas.winfo_width()
        count = 35 if self.streak >= 10 else 22
        particles = []
        for _ in range(count):
            x = random.randint(10, max(11, cw - 10))
            y = random.randint(-60, -5)
            size = random.randint(6, 14)
            color = random.choice(CONFETTI_COLORS)
            if random.random() < 0.5:
                item = self.letter_canvas.create_oval(
                    x, y, x + size, y + size, fill=color, outline='', tags='confetti')
            else:
                item = self.letter_canvas.create_rectangle(
                    x, y, x + size, y + size // 2, fill=color, outline='', tags='confetti')
            # Keep confetti below the letter text
            self.letter_canvas.tag_lower(item, self.shadow_id)
            particles.append({'id': item, 'vx': random.uniform(-1.5, 1.5),
                               'vy': random.uniform(3.5, 7.0)})
        self.animate_confetti(particles, 0)

    def animate_confetti(self, particles, step):
        if step >= 48:
            self.letter_canvas.delete('confetti')
            return
        ch = self.letter_canvas.winfo_height()
        alive = []
        for p in particles:
            self.letter_canvas.move(p['id'], p['vx'], p['vy'])
            p['vy'] += 0.15
            coords = self.letter_canvas.coords(p['id'])
            if coords and coords[1] < ch + 20:
                alive.append(p)
        if alive:
            self.root.after(28, lambda: self.animate_confetti(alive, step + 1))
        else:
            self.letter_canvas.delete('confetti')

    # ------------------------------------------------------------------
    # Resize
    # ------------------------------------------------------------------

    def on_resize(self, event):
        if event.widget != self.root:
            return
        cw = self.letter_canvas.winfo_width()
        ch = self.letter_canvas.winfo_height()
        if cw < 2 or ch < 2:
            return
        font_size = min(cw, ch) * 3 // 4
        font_size = max(50, min(font_size, 300))
        self.letter_size = font_size
        font = ('Arial', font_size, 'bold')
        self.letter_canvas.itemconfig(self.letter_id, font=font)
        self.letter_canvas.itemconfig(self.shadow_id, font=font)
        self._place_letter()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A typing game for youngsters')
    parser.add_argument('-letters', action='store_true', help='Enable letters (A-Z)')
    parser.add_argument('-numbers', action='store_true', help='Enable numbers (0-9)')
    args = parser.parse_args()

    use_letters = args.letters or not (args.letters or args.numbers)
    use_numbers = args.numbers

    game = TypingGame(use_letters, use_numbers)
    game.run()
