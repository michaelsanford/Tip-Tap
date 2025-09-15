#!/usr/bin/env python3
"""A typing game for youngsters."""

import tkinter as tk
import random

# ASCII art for letters A-Z
ASCII_LETTERS = {
    'A': [
        "        AAAAAAAAAA        ",
        "       AAAAAAAAAAAA       ",
        "      AAAAA    AAAAA      ",
        "     AAAAA      AAAAA     ",
        "    AAAAA        AAAAA    ",
        "   AAAAA          AAAAA   ",
        "  AAAAA            AAAAA  ",
        " AAAAA              AAAAA ",
        "AAAAAAAAAAAAAAAAAAAAAAAAAA",
        "AAAAAAAAAAAAAAAAAAAAAAAAAA",
        "AAAAA                AAAAA",
        "AAAAA                AAAAA",
        "AAAAA                AAAAA",
        "AAAAA                AAAAA"
    ],
    'B': [
        "BBBBBBBBBBBBBBBBBBBBBBBBB",
        "BBBBBBBBBBBBBBBBBBBBBBBBBB",
        "BBBBB                BBBBB",
        "BBBBB                BBBBB",
        "BBBBB                BBBBB",
        "BBBBBBBBBBBBBBBBBBBBBBBBBB",
        "BBBBBBBBBBBBBBBBBBBBBBBBBB",
        "BBBBB                BBBBB",
        "BBBBB                BBBBB",
        "BBBBB                BBBBB",
        "BBBBB                BBBBB",
        "BBBBBBBBBBBBBBBBBBBBBBBBBB",
        "BBBBBBBBBBBBBBBBBBBBBBBBBB",
        "BBBBBBBBBBBBBBBBBBBBBBBBB"
    ],
    'C': [
        "   CCCCCCCCCCCCCCCCCCCCC   ",
        "  CCCCCCCCCCCCCCCCCCCCCCC  ",
        " CCCCC               CCCCC ",
        "CCCCC",
        "CCCCC",
        "CCCCC",
        "CCCCC",
        "CCCCC",
        "CCCCC",
        "CCCCC",
        "CCCCC",
        " CCCCC               CCCCC ",
        "  CCCCCCCCCCCCCCCCCCCCCCC  ",
        "   CCCCCCCCCCCCCCCCCCCCC   "
    ],
    'D': [
        "DDDDDDDDDDDDDDDDDDDDDDDD",
        "DDDDDDDDDDDDDDDDDDDDDDDDD",
        "DDDDD               DDDDD",
        "DDDDD                DDDDD",
        "DDDDD                DDDDD",
        "DDDDD                DDDDD",
        "DDDDD                DDDDD",
        "DDDDD                DDDDD",
        "DDDDD                DDDDD",
        "DDDDD                DDDDD",
        "DDDDD               DDDDD",
        "DDDDDDDDDDDDDDDDDDDDDDDDD",
        "DDDDDDDDDDDDDDDDDDDDDDDD"
    ],
    'E': [
        "EEEEEEEEEEEEEEEEEEEEEEEEEE",
        "EEEEEEEEEEEEEEEEEEEEEEEEEE",
        "EEEEE",
        "EEEEE",
        "EEEEE",
        "EEEEE",
        "EEEEEEEEEEEEEEEEEEEE",
        "EEEEEEEEEEEEEEEEEEEE",
        "EEEEE",
        "EEEEE",
        "EEEEE",
        "EEEEE",
        "EEEEEEEEEEEEEEEEEEEEEEEEEE",
        "EEEEEEEEEEEEEEEEEEEEEEEEEE"
    ],
    'F': [
        "FFFFFFFFFFFFFFFFFFFFFFFFFF",
        "FFFFFFFFFFFFFFFFFFFFFFFFFF",
        "FFFFF",
        "FFFFF",
        "FFFFF",
        "FFFFF",
        "FFFFFFFFFFFFFFFFFFFFFF",
        "FFFFFFFFFFFFFFFFFFFFFF",
        "FFFFF",
        "FFFFF",
        "FFFFF",
        "FFFFF",
        "FFFFF",
        "FFFFF"
    ],
    'G': [
        "   GGGGGGGGGGGGGGGGGGGGG   ",
        "  GGGGGGGGGGGGGGGGGGGGGGG  ",
        " GGGGG               GGGGG ",
        "GGGGG",
        "GGGGG",
        "GGGGG",
        "GGGGG",
        "GGGGG         GGGGGGGGGGGG",
        "GGGGG         GGGGGGGGGGGG",
        "GGGGG                GGGGG",
        "GGGGG                GGGGG",
        " GGGGG              GGGGG",
        "  GGGGGGGGGGGGGGGGGGGGGGG  ",
        "   GGGGGGGGGGGGGGGGGGGGG   "
    ],
    'H': [
        "HHHHH                HHHHH",
        "HHHHH                HHHHH",
        "HHHHH                HHHHH",
        "HHHHH                HHHHH",
        "HHHHH                HHHHH",
        "HHHHH                HHHHH",
        "HHHHHHHHHHHHHHHHHHHHHHHHHH",
        "HHHHHHHHHHHHHHHHHHHHHHHHHH",
        "HHHHH                HHHHH",
        "HHHHH                HHHHH",
        "HHHHH                HHHHH",
        "HHHHH                HHHHH",
        "HHHHH                HHHHH",
        "HHHHH                HHHHH"
    ],
    'I': [
        "IIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIII",
        "         IIIII",
        "         IIIII",
        "         IIIII",
        "         IIIII",
        "         IIIII",
        "         IIIII",
        "         IIIII",
        "         IIIII",
        "         IIIII",
        "         IIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIII",
        "IIIIIIIIIIIIIIIIIIIIIIIIII"
    ],
    'J': [
        "JJJJJJJJJJJJJJJJJJJJJJJJJJ",
        "JJJJJJJJJJJJJJJJJJJJJJJJJJ",
        "                 JJJJJ",
        "                 JJJJJ",
        "                 JJJJJ",
        "                 JJJJJ",
        "                 JJJJJ",
        "                 JJJJJ",
        "                 JJJJJ",
        "JJJJJ            JJJJJ",
        "JJJJJ            JJJJJ",
        " JJJJJ          JJJJJ",
        "  JJJJJJJJJJJJJJJJJJ",
        "   JJJJJJJJJJJJJJJJ"
    ],
    'K': [
        "KKKKK              KKKKKK",
        "KKKKK            KKKKKK",
        "KKKKK          KKKKKK",
        "KKKKK        KKKKKK",
        "KKKKK      KKKKKK",
        "KKKKK    KKKKKK",
        "KKKKKKKKKKK",
        "KKKKKKKKKKK",
        "KKKKK    KKKKKK",
        "KKKKK      KKKKKK",
        "KKKKK        KKKKKK",
        "KKKKK          KKKKKK",
        "KKKKK            KKKKKK",
        "KKKKK              KKKKKK"
    ],
    'L': [
        "LLLLL",
        "LLLLL",
        "LLLLL",
        "LLLLL",
        "LLLLL",
        "LLLLL",
        "LLLLL",
        "LLLLL",
        "LLLLL",
        "LLLLL",
        "LLLLL",
        "LLLLL",
        "LLLLLLLLLLLLLLLLLLLLLLLLLL",
        "LLLLLLLLLLLLLLLLLLLLLLLLLL"
    ],
    'M': [
        "MMMMM                MMMMM",
        "MMMMMM              MMMMMM",
        "MMMMMMM            MMMMMMM",
        "MMMMMMMM          MMMMMMMM",
        "MMMMM MMMM      MMMM MMMMM",
        "MMMMM  MMMM    MMMM  MMMMM",
        "MMMMM   MMMM  MMMM   MMMMM",
        "MMMMM    MMMMMMMM    MMMMM",
        "MMMMM     MMMMMM     MMMMM",
        "MMMMM      MMMM      MMMMM",
        "MMMMM       MM       MMMMM",
        "MMMMM                MMMMM",
        "MMMMM                MMMMM",
        "MMMMM                MMMMM"
    ],
    'N': [
        "NNNNN                NNNNN",
        "NNNNNN               NNNNN",
        "NNNNNNN              NNNNN",
        "NNNNNNNN             NNNNN",
        "NNNNN NNNN           NNNNN",
        "NNNNN  NNNN          NNNNN",
        "NNNNN   NNNN         NNNNN",
        "NNNNN    NNNN        NNNNN",
        "NNNNN     NNNN       NNNNN",
        "NNNNN      NNNN      NNNNN",
        "NNNNN       NNNN     NNNNN",
        "NNNNN        NNNN    NNNNN",
        "NNNNN         NNNNNNNNNNN",
        "NNNNN          NNNNNNNNNN"
    ],
    'O': [
        "   OOOOOOOOOOOOOOOOOOOOO   ",
        "  OOOOOOOOOOOOOOOOOOOOOOO  ",
        " OOOOO               OOOOO ",
        "OOOOO                 OOOOO",
        "OOOOO                 OOOOO",
        "OOOOO                 OOOOO",
        "OOOOO                 OOOOO",
        "OOOOO                 OOOOO",
        "OOOOO                 OOOOO",
        "OOOOO                 OOOOO",
        "OOOOO                 OOOOO",
        " OOOOO               OOOOO ",
        "  OOOOOOOOOOOOOOOOOOOOOOO  ",
        "   OOOOOOOOOOOOOOOOOOOOO   "
    ],
    'P': [
        "PPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPP                PPPPP",
        "PPPPP                PPPPP",
        "PPPPP                PPPPP",
        "PPPPP                PPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPP",
        "PPPPP",
        "PPPPP",
        "PPPPP",
        "PPPPP",
        "PPPPP"
    ],
    'Q': [
        "   QQQQQQQQQQQQQQQQQQQQQ   ",
        "  QQQQQQQQQQQQQQQQQQQQQQQ  ",
        " QQQQQ               QQQQQ ",
        "QQQQQ                 QQQQQ",
        "QQQQQ                 QQQQQ",
        "QQQQQ                 QQQQQ",
        "QQQQQ                 QQQQQ",
        "QQQQQ                 QQQQQ",
        "QQQQQ         QQQ     QQQQQ",
        "QQQQQ          QQQQ   QQQQQ",
        "QQQQQ           QQQQQQQQQQ",
        " QQQQQ           QQQQQQQQ",
        "  QQQQQQQQQQQQQQQQQQQQQ",
        "   QQQQQQQQQQQQQQQQQQ  QQ"
    ],
    'R': [
        "RRRRRRRRRRRRRRRRRRRRRRRRRR",
        "RRRRRRRRRRRRRRRRRRRRRRRRR",
        "RRRRR                RRRRR",
        "RRRRR                RRRRR",
        "RRRRR                RRRRR",
        "RRRRR                RRRRR",
        "RRRRRRRRRRRRRRRRRRRRRRRRR",
        "RRRRRRRRRRRRRRRRRRRRRRRR",
        "RRRRR        RRRRRR",
        "RRRRR          RRRRRR",
        "RRRRR            RRRRRR",
        "RRRRR              RRRRRR",
        "RRRRR                RRRRR",
        "RRRRR                RRRRR"
    ],
    'S': [
        "   SSSSSSSSSSSSSSSSSSSSS   ",
        "  SSSSSSSSSSSSSSSSSSSSSSS  ",
        " SSSSS               SSSSS",
        "SSSSS",
        "SSSSS",
        " SSSSS",
        "  SSSSSSSSSSSSSSSSSSSS",
        "   SSSSSSSSSSSSSSSSSSSSSS",
        "                     SSSSS",
        "                      SSSSS",
        "                      SSSSS",
        " SSSSS               SSSSS",
        "  SSSSSSSSSSSSSSSSSSSSSSS  ",
        "   SSSSSSSSSSSSSSSSSSSSS   "
    ],
    'T': [
        "TTTTTTTTTTTTTTTTTTTTTTTTTT",
        "TTTTTTTTTTTTTTTTTTTTTTTTTT",
        "          TTTTT",
        "          TTTTT",
        "          TTTTT",
        "          TTTTT",
        "          TTTTT",
        "          TTTTT",
        "          TTTTT",
        "          TTTTT",
        "          TTTTT",
        "          TTTTT",
        "          TTTTT",
        "          TTTTT"
    ],
    'U': [
        "UUUUU                 UUUUU",
        "UUUUU                 UUUUU",
        "UUUUU                 UUUUU",
        "UUUUU                 UUUUU",
        "UUUUU                 UUUUU",
        "UUUUU                 UUUUU",
        "UUUUU                 UUUUU",
        "UUUUU                 UUUUU",
        "UUUUU                 UUUUU",
        "UUUUU                 UUUUU",
        "UUUUU                 UUUUU",
        " UUUUU               UUUUU",
        "  UUUUUUUUUUUUUUUUUUUUUUU",
        "   UUUUUUUUUUUUUUUUUUUUU"
    ],
    'V': [
        "VVVVV                 VVVVV",
        "VVVVV                 VVVVV",
        "VVVVV                 VVVVV",
        "VVVVV                 VVVVV",
        "VVVVV                 VVVVV",
        " VVVVV               VVVVV",
        " VVVVV               VVVVV",
        "  VVVVV             VVVVV",
        "   VVVVV           VVVVV",
        "    VVVVV         VVVVV",
        "     VVVVV       VVVVV",
        "      VVVVV     VVVVV",
        "       VVVVVVVVVVVVV",
        "        VVVVVVVVVVV"
    ],
    'W': [
        "WWWWW                 WWWWW",
        "WWWWW                 WWWWW",
        "WWWWW                 WWWWW",
        "WWWWW                 WWWWW",
        "WWWWW        W        WWWWW",
        "WWWWW       WWW       WWWWW",
        "WWWWW      WWWWW      WWWWW",
        "WWWWW     WWWWWWW     WWWWW",
        "WWWWW    WWWW WWWW    WWWWW",
        "WWWWW   WWWW   WWWW   WWWWW",
        "WWWWW  WWWW     WWWW  WWWWW",
        "WWWWW WWWW       WWWW WWWWW",
        "WWWWWWWWW         WWWWWWWWW",
        "WWWWWWWW           WWWWWWWW"
    ],
    'X': [
        "XXXXX                 XXXXX",
        " XXXXX               XXXXX",
        "  XXXXX             XXXXX",
        "   XXXXX           XXXXX",
        "    XXXXX         XXXXX",
        "     XXXXX       XXXXX",
        "      XXXXXXXXXXXXXXXX",
        "       XXXXXXXXXXXXXX",
        "      XXXXXXXXXXXXXXXX",
        "     XXXXX       XXXXX",
        "    XXXXX         XXXXX",
        "   XXXXX           XXXXX",
        "  XXXXX             XXXXX",
        " XXXXX               XXXXX"
    ],
    'Y': [
        "YYYYY                 YYYYY",
        " YYYYY               YYYYY",
        "  YYYYY             YYYYY",
        "   YYYYY           YYYYY",
        "    YYYYY         YYYYY",
        "     YYYYY       YYYYY",
        "      YYYYY     YYYYY",
        "       YYYYYYYYYYYYYYY",
        "        YYYYYYYYYYY",
        "          YYYYY",
        "          YYYYY",
        "          YYYYY",
        "          YYYYY",
        "          YYYYY"
    ],
    'Z': [
        "ZZZZZZZZZZZZZZZZZZZZZZZZZZ",
        "ZZZZZZZZZZZZZZZZZZZZZZZZZZ",
        "                    ZZZZZ",
        "                  ZZZZZ",
        "                ZZZZZ",
        "              ZZZZZ",
        "            ZZZZZ",
        "          ZZZZZ",
        "        ZZZZZ",
        "      ZZZZZ",
        "    ZZZZZ",
        "  ZZZZZ",
        "ZZZZZZZZZZZZZZZZZZZZZZZZZZ",
        "ZZZZZZZZZZZZZZZZZZZZZZZZZZ"
    ]
}

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

    def __init__(self):
        """Initialize the typing game."""
        self.score = 0
        self.color_index = 0
        self.target_letter = None
        self.root = tk.Tk()
        self.root.title("Tip-Tap Typing Game")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.focus_set()

        # Create main frame that centers content
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.score_label = tk.Label(self.main_frame, text=f"Score: {self.score}",
                                   font=('Courier', 16), fg='cyan', bg='black')
        self.score_label.pack(pady=10)

        self.letter_label = tk.Label(self.main_frame, text="",
                                    font=('Courier', 10), fg='#00FF41', bg='black',
                                    justify='left')
        self.letter_label.pack(pady=20)

        self.prompt_label = tk.Label(self.main_frame, text="Press any key to start!",
                                    font=('Courier', 14), fg='cyan', bg='black')
        self.prompt_label.pack(pady=10)

        self.response_label = tk.Label(self.main_frame, text="",
                                      font=('Courier', 14), fg='green', bg='black')
        self.response_label.pack(pady=10)

        self.new_round()

    def new_round(self):
        """Start a new round with a random letter."""
        self.target_letter = random.choice(list(ASCII_LETTERS.keys()))
        ascii_art = '\n'.join(ASCII_LETTERS[self.target_letter])
        # Replace letters with block characters for prettier display
        pretty_art = ascii_art.replace(self.target_letter, '█')

        # Cycle through colors
        current_color = COLORS[self.color_index]
        self.color_index = (self.color_index + 1) % len(COLORS)

        self.letter_label.config(text=pretty_art, fg=current_color)
        self.prompt_label.config(text=f"Press the '{self.target_letter}' key!")
        self.response_label.config(text="")

    def flash_screen(self):
        """Flash the screen green for correct answer."""
        # Flash green
        self.root.configure(bg='#00FF00')
        self.main_frame.configure(bg='#00FF00')
        self.root.after(150, self.restore_colors)
        
    def restore_colors(self):
        """Restore original colors after flash."""
        self.root.configure(bg='black')
        self.main_frame.configure(bg='black')

    def on_key_press(self, event):
        """Handle key press events."""
        pressed_key = event.char.upper()

        if pressed_key == self.target_letter:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            response = random.choice(JOYFUL_RESPONSES)
            self.response_label.config(text=response, fg='green')
            self.flash_screen()
            self.root.after(1500, self.new_round)
        elif pressed_key.isalpha():
            error_msg = f"Oops! You pressed '{pressed_key}', try '{self.target_letter}'"
            self.response_label.config(text=error_msg, fg='red')

    def run(self):
        """Start the game main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    game = TypingGame()
    game.run()