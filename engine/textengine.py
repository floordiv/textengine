import os
import json
import time
import platform
from time import sleep
from getch import getch


cls = 'cls' if platform.system().lower() == "windows" else 'clear'


class resources:
    pass


class area:
    __content = []

    @staticmethod
    def init():
        init_map_spaces = ' ' if settings.area_map_type == 'letter' else settings.area_map_object_bindings[' ']
        for each in range(settings.screen_resolution[1]):
            temp = []
            for point in range(settings.screen_resolution[0]):
                temp.append(init_map_spaces)
            area.__content.append(temp)

    @staticmethod
    def clear():
        os.system(cls)

    @staticmethod
    def draw(text_under=False, timer=3):
        area.clear()
        print(settings.area_map_object_bindings[settings.area_map_bindings['horizontal-border']] *
              settings.screen_resolution[0])
        vertical_border = settings.area_map_object_bindings[settings.area_map_bindings['vertical-border']]
        for index, x_line in enumerate(area.__content):
            print(vertical_border + ''.join(area.__content[index]) + vertical_border)
        print(settings.area_map_object_bindings[settings.area_map_bindings['horizontal-border']] *
              settings.screen_resolution[0])
        if var.area_draw_text:
            if float(var.area_draw_text_started_at) < float(var.area_draw_text_timer):
                print(var.area_draw_text_value)
            else:
                var.area_draw_text = False
        elif text_under and not var.area_draw_text:
            var.area_draw_text = True
            var.area_draw_text_started_at = time.time()
            var.area_draw_text_timer = timer
            var.area_draw_text_value = text_under
            print(text_under)

    @staticmethod
    def reload(source, save_player_pos=False):
        if not save_player_pos:
            player.move([0, 0], reset=True)

    @staticmethod
    def broadcast(*text, position='on_screen', align='center', close_on='action', timer=3):
        text = ' '.join(text)
        old_area_under_text = ''
        if position == 'on_screen':
            pos = tui.align_position(len(text), align)
            y_pos, start, end = pos
            if not pos:
                y_pos, start, end = tui.align_position(len(text), 'top')
            old_area_under_text = ''.join(area.__content[y_pos][start:end + 1])
            area.__content[y_pos][start:end + 1] = [text]
        elif position == 'under_screen':
            area.draw(text_under=text)
        if close_on == 'action' and position != 'under_screen':
            any_input = getch()
            area.__content[y_pos][start:end + 1] = [old_area_under_text]
            return any_input
        elif close_on == 'timer':
            sleep(timer)


class var:
    area_draw_text = False
    area_draw_text_started_at = 0
    area_draw_text_timer = 0
    area_draw_text_value = ''


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

    @staticmethod
    def align_position(text, align):
        text = len(text)
        if align == 'center':
            zero_pos = settings.screen_resolution[0] // 2
            y_pos = settings.screen_resolution[1] // 2
            start = zero_pos - (text // 2)
            finish = zero_pos + (text - text // 2)
            return [y_pos, start, finish]
        elif align == 'right':
            return [settings.screen_resolution[1] // 2, settings.screen_resolution[0] - text, settings.screen_resolution[0]]
        elif align == 'left':
            return [settings.screen_resolution[1] // 2, settings.screen_resolution[0]], settings.screen_resolution[0] + text,
        elif align == 'top':
            zero_pos = settings.screen_resolution[0] // 2
            start = zero_pos - (text // 2)
            finish = zero_pos + (text - text // 2)
            return [0, start, finish]
        elif align == 'bottom':
            zero_pos = settings.screen_resolution[0] // 2
            start = zero_pos - (text // 2)
            finish = zero_pos + (text - text // 2)
            return [settings.screen_resolution[1], start, finish]
        return False


class settings:
    player_max_steps_per_move = 1
    screen_resolution = [40, 25]  # 40x25, x, y
    console_enable = False
    cheats_detect = False
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
    area_map_type = 'letter'
    area_map = None
    area_map_object_bindings = {
        0: ' ',
        1: '|',
        2: '—',
        3: '@',
        4: '#',
        5: '~',
        6: 'X',
        7: 'O'  # etc.
    }
    area_map_bindings = {
        'border': 0,
        'horizontal-border': 1,
        'vertical-border': 2,
        'tree': 3,
        'water': 4,
        'object': 5,
        'x_player': 6,
        'y_player': 7
    }


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
    area.init()
    return True
