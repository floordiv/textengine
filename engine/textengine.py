import os
import log
import json
import time
import platform
from time import sleep
from getch import getch


version = '1.2.1'
cls = 'cls' if platform.system().lower() == "windows" else 'clear'


class resources:
    pass


class area:
    __content = []
    collision_objects = []
    objects = {}

    @staticmethod
    def init():
        init_map_spaces = ' ' if settings.area_map_type == 'letter' else settings.area_map_object_bindings[' ']
        for each in range(settings.screen_resolution[1] + 1):
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
              (settings.screen_resolution[0] + 2))
        vertical_border = settings.area_map_object_bindings[settings.area_map_bindings['vertical-border']]
        for index, x_line in enumerate(area.__content):
            print(vertical_border + ''.join(area.__content[index]) + vertical_border)
        print(settings.area_map_object_bindings[settings.area_map_bindings['horizontal-border']] *
              (settings.screen_resolution[0] + 2))
        if text_under and timer == 0:
            print(text_under)
            text_under = False
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
            player.move([5, 5], reset=True)

    @staticmethod
    def add_object(obj, coords, collision=False):
        if collision:
            area.collision_objects.append(coords)
        area.objects[obj] = coords
        area.__content[coords[1]][coords[0]] = obj

    @staticmethod
    def get_obj(coords):
        return area.__content[coords[1]][coords[0]]

    @staticmethod
    def remove_player():
        coords = var.player_last_pos
        area.__content[coords[1]][coords[0]] = ' '

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
    player_model = '*'
    homepath = '..'
    player_last_pos = [0, 0]
    player_previous_obj = ' '
    player_trail = False


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
    default_player_pos = [5, 0]  # x, y
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
        'vertical-border': 1,
        'horizontal-border': 2,
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
            if source in os.listdir(f'{var.homepath}/resources'):
                with open(f'{var.homepath}/resources/{source}', 'r') as player_model:
                    player_model = player_model.read().split('\n')[0][0]    # only 1-letter player supported (currently)
                    var.player_model = player_model
                return True
            raise FileNotFoundError(f'resources: source: {var.homepath}/resources/{source}')

        @staticmethod
        def remove(name):
            pass

        @staticmethod
        def reload(source, x=0, y=0):
            pass

        @staticmethod
        def get():
            return var.player_model

    @staticmethod
    def teleport(coords):
        area.remove_player()
        area.add_object('*', coords)

    @staticmethod
    def is_collision(coord_type, current_coord, new_coord):     # simplified function, does not in use
        # please, do not forget to remove it
        if current_coord + new_coord == -1 or current_coord + new_coord ==\
                settings.screen_resolution[0 if coord_type == 'x' else 1] + (1 if coord_type == 'y' else 0):
            return True
        return False

    @staticmethod
    def is_collision_object(new_coords):
        pass

    @staticmethod
    def collision(new_coords):
        current_coords = player.get_coords()
        new_player_coords = [current_coords[0] + new_coords[0], current_coords[1] + new_coords[1]]
        check_x_coord = True if new_coords[1] == 0 else False
        if new_player_coords[0] < 0 or new_player_coords[0] >= settings.screen_resolution[0] and check_x_coord:  # x coords check
            return True
        if new_player_coords[1] < 0 or new_player_coords[1] >= settings.screen_resolution[1] + 1 and not check_x_coord:  # y coords check
            return True
        if new_player_coords in area.collision_objects:     # if possible move goes to the collision object
            return True
        return False

    @staticmethod
    def get_coords():
        return [player.__x, player.__y]

    @staticmethod
    def move(new_coords, reset=False):  # list ([x, y])
        if reset:
            player.__x = settings.default_player_pos[0]
            player.__y = settings.default_player_pos[1]
            return
        x = new_coords[0] + player.__x
        y = new_coords[1] + player.__y
        steps_area = list(range(-settings.player_max_steps_per_move, settings.player_max_steps_per_move + 1))
        if x not in steps_area or y not in steps_area:
            if settings.cheats_detect:
                raise Exception('cheating: player jumped over max steps number')
        is_collision = player.collision(new_coords)
        future_symbol = area.get_obj([x, y] if not is_collision else [player.__x, player.__y])
        temp_previous_obj = ' ' if not var.player_trail else '*'
        if future_symbol != ' ':
            temp_previous_obj = future_symbol
        var.player_last_pos = [player.__x, player.__y]
        if not is_collision:
            player.__x = x
            player.__y = y
            if not var.player_trail:
                area.remove_player()
            area.add_object(var.player_model, [player.__x, player.__y])
            area.add_object(var.player_previous_obj, [player.__x - new_coords[0], player.__y - new_coords[1]])
            var.player_previous_obj = temp_previous_obj


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

    var.homepath = homepath

    for setting in all_settings:
        if os.path.exists(f'{homepath}/config/{setting}'):
            with open(f'{homepath}/config/{setting}') as config:
                raw_settings = json.load(config)
            for each in raw_settings:
                setattr(settings, each, raw_settings[each])
    area.init()
    player.move([], reset=True)
    return True
