"""Simple CLI UI functions that aren't dependent on chempare module"""

import os
from typing import NoReturn


#
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# ESC Code Sequence	Description
# -----------------   -----------
# ESC[?25l	        make cursor invisible
# ESC[?25h	        make cursor visible
# ESC[?47l	        restore screen
# ESC[?47h	        save screen
# ESC[?1049h	        enables the alternative buffer
# ESC[?1049l	        disables the alternative buffer
#


def goto_home() -> NoReturn:
    """Goes to the home cursor location"""
    print("\033[H")


def clear_below_line(line: int = 2) -> NoReturn:
    """Clears terminal from this line and below"""
    print(f"\033[{line}J")


def clear_screen() -> NoReturn:
    """Should be similar to typing 'clear'"""
    print("\033c")
    # print("\033]50;ClearScrollback\a") # Used for iterm only, idk why


def create_alt_buffer() -> NoReturn:
    """Creates a new output buffer. Useful for if you want to 'clear' the screen but restore it later"""
    # \033[?1049h - creates new terminal, cursor remains where it was (tput rmcup)
    print("\033[?1049h")
    # goto_home()


def rm_alt_buffer() -> NoReturn:
    """Restores the screen to the old buffer"""
    # Same as tput smcup
    print("\033[?1049l")


def kill_self() -> NoReturn:
    """Kills self and all child processes. Better than sys.exit() or os._exit()"""
    os.system(f"kill -3 {os.getpid()}")
    raise SystemExit


def reset_term() -> NoReturn:
    """Resets terminal"""
    print("\033c")
    # print("\033\143")


def goto_line(line: int) -> NoReturn:
    """Goes to specific line in terminal"""
    print(f"\033[{line}J")


def enable_line_drawing() -> NoReturn:
    print("\033(0")


def disable_line_drawing() -> NoReturn:
    print("\033(B")
