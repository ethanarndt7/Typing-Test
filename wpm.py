import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr('Welcome to the Typing Test!')
    stdscr.addstr('\nPress any key to begin!')
    stdscr.refresh()
    stdscr.getkey()   # allows user to exit start screen

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f'WPM: {wpm}')

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)   # shows red color if user types incorrectly

        stdscr.addstr(0, i, char, color)   # displays user text in different color


def wpm_test(stdscr):
    target_text = 'The quick brown fox jumps over the lazy dog.'
    current_text = []
    wpm = 0
    start_time = time.time()    # keeps track of start time
    stdscr.nodelay(True)    # allows wpm counter to run without user typing

    
    while True:
        time_elapsed = max(time.time() - start_time, 1)   # calculates time
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)  # calculates words per min (avg word has 5 characters)


        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if ''.join(current_text) == target_text:
            stdscr.nodelay(False)   # stops wpm counter if user completed type test
            break
        
        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # allows user to press ESC to exit
            break

        if key in ('KEY_BACKSPACE', '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()  # removes last element from list
        elif len(current_text) < len(target_text):
            current_text.append(key)    # adds keys user pressed to current_text
        


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    start_screen(stdscr)
    while True:     # allows user to play again 
        wpm_test(stdscr)
        stdscr.addstr(2, 0, 'Congratulations! You completed the test! Press any key to play again. Press ESC to exit')
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main)   # call main to wrapper to utilize curses library
