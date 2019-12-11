import os
import json
import platform

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

class settings:
    max_steps_per_move = 1
    resolution = [40, 25]   # 40x25
    binds = {"move_up": "w",
             "move_down": "s",
             "move_left": "a",
             "move_right": "d",
             "action_inventory": b'\t'}
    default_player_pos = [0, 0]     # x, y


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
    def move(new_coords, reset=False):   # list ([x, y])
        if reset:
            player.__x = settings.default_player_pos[0]
            player.__y = settings.default_player_pos[1]
            return
        x = new_coords[0]
        y = new_coords[1]
        steps_area = list(range(-settings.max_steps_per_move, settings.max_steps_per_move + 1))
        if x not in steps_area or y not in steps_area:
            raise Exception('cheating: player jumped over max steps number')
        player.__x += x
        player.__y += y


def close():
    import sys
    sys.exit()


def fix_configs(*configs):
    pass


def init(homepath='..'):    # from where will be engine ran
    all_settings = ['keybindings', 'player', 'resolution']

    for setting in all_settings:
        with open(f'{homepath}/config/{setting}') as config:
            raw_settings = json.load(config)

