import os
import datetime


def write(*text):
    text = ' '.join(text)
    mode = 'a' if 'debug' in os.listdir() else 'w'
    with open('debug', mode) as log_file:
        log_file.write(f'[{datetime.datetime.now()}] {text}\n')
