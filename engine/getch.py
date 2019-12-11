import platform
getch_func = __import__(platform.system().lower())


def getch():
    return getch_func.getch()
