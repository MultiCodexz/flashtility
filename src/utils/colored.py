# app/src/utils/colored.py
import curses
import time
import random

COLORS = [curses.COLOR_RED, curses.COLOR_GREEN, curses.COLOR_YELLOW,
          curses.COLOR_BLUE, curses.COLOR_MAGENTA, curses.COLOR_CYAN]

def println(text, bounce=False, delay=0.05):
    if not bounce:
        words = text.split()
        colored_words = []
        for w in words:
            color = random.choice(COLORS)
            colored_words.append(f"{curses.color_pair(color)}{w}\033[0m")
        print(" ".join(colored_words))
    else:
        # Bounce: buchstabe für buchstabe animiert
        for i, char in enumerate(text):
            if i % 2 == 0:
                print("\n" + char, end='', flush=True)
            else:
                print("\033[F" + char, end='', flush=True)
            time.sleep(delay)
        print()
