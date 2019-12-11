import os
import json
import platform
from getch import getch


cls = 'cls' if platform.system().lower() == "windows" else 'clear'


class resources:
    pass


class area:
    @staticmethod
    def clear():
        os.system(cls)

    @staticmethod
    def draw():
        pass

    @staticmethod
    def reload(source, save_player_pos=False):
        if not save_player_pos:
            player.move([0, 0], reset=True)


class tui:
    @staticmethod
    def _draw_menu(menu_text, options, active_option):
        index = 0
        print(menu_text)
        for option in options:
            print('> ' + option if index == active_option else option)
            index += 1

    @staticmethod
    def menu(menu_text, options, show_hint=True):  # dict with codes
        os.system(cls)
        active_option = 0
        chose = False
        keys = {
            'w': -1,
            's': 1
        }
        if show_hint:
            menu_text = 'Hint: w and s to scroll, f to choose\n' + menu_text
        tui._draw_menu(menu_text, options, active_option)
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
                tui._draw_menu(menu_text, options, active_option)
            elif pressed_key == 'f':
                chose = True

        return options[list(options)[active_option]]


class settings:
    player_max_steps_per_move = 1
    screen_resolution = [40, 25]  # 40x25
    console_enable = False
    keybindings_move_binds = {
        'up': b'w',
        'down': b's',
        'left': b'a',
        'right': b'd'
    }
    keybindings_action_binds = {
        'inventory': b'\t',
        'menu': b'\x1b',
        'sitdown': b'c',
        'liedown': b'x',
        'interact': b'f',
        'chat': b't',
        'console': b'`'
    }
    default_player_pos = [0, 0]  # x, y


class player:
    __x = 0
    __y = 0

    class model:
        @staticmethod
        def load(source):
            pass

        @staticmethod
        def remove(name):
            pass

        @staticmethod
        def reload(source, x=0, y=0):
            pass

    @staticmethod
    def get_coords():
        return [player.__x, player.__y]

    @staticmethod
    def move(new_coords, reset=False):  # list ([x, y])
        if reset:
            player.__x = settings.default_player_pos[0]
            player.__y = settings.default_player_pos[1]
            return
        x = new_coords[0]
        y = new_coords[1]
        steps_area = list(range(-settings.player_max_steps_per_move, settings.player_max_steps_per_move + 1))
        if x not in steps_area or y not in steps_area:
            raise Exception('cheating: player jumped over max steps number')
        player.__x += x
        player.__y += y


def close():
    import sys
    sys.exit()


def fix_configs(*configs):
    pass


def runcmd(cmd):
    if settings.console_enable:
        try:
            eval(cmd)   # it is unsecure, I know. But idk, how to protect engine
        except Exception as console_cmd_run_exception:
            print('[ERROR]', console_cmd_run_exception)


def init(homepath='..'):  # from where will be engine ran
    all_settings = ['keybindings', 'player', 'screen']

    for setting in all_settings:
        if os.path.exists(f'{homepath}/config/{setting}'):
            with open(f'{homepath}/config/{setting}') as config:
                raw_settings = json.load(config)
            for each in raw_settings:
                setattr(settings, each, raw_settings[each])
    return True
