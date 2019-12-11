import os
import sys
import select
import termios
import platform


cls = 'cls' if platform.system().lower() == "windows" else 'clear'


def _draw_menu(menu_text, options, active_option):
    index = 0
    print(menu_text)
    for option in options:
        print('> ' + option if index == active_option else option)
        index += 1


def menu(menu_text, options, show_hint=True):      # dict with codes
    os.system(cls)
    active_option = 0
    chose = False
    keys = {
        'w': -1,
        's': 1
    }
    if show_hint:
        menu_text = 'Hint: w and s to scroll, f to choose\n' + menu_text
    _draw_menu(menu_text, options, active_option)
    while not chose:
        pressed_key = getch()
        if pressed_key in ['w', 's']:
            active_option += keys[pressed_key]
            try:
                list(options)[active_option]
            except IndexError:
                active_option += -keys[pressed_key]
            finally:
                if active_option < 0:
                    active_option = 0
            os.system(cls)
            _draw_menu(menu_text, options, active_option)
        elif pressed_key == 'f':
            chose = True

    return options[list(options)[active_option]]


def getch(timeout=None):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        setup_term(fd)
        try:
            rw, wl, xl = select.select([fd], [], [], timeout)
        except select.error:
            return
        if rw:
            return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def setup_term(fd, when=termios.TCSAFLUSH):
    mode = termios.tcgetattr(fd)
    mode[tty.LFLAG] = mode[tty.LFLAG] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(fd, when, mode)
