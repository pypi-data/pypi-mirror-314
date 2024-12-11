
import sys
import itertools
import time
import threading


def spinner(message: str):
    spinner = itertools.cycle(["|", "/", "-", "\\"])
    stop_flag = [False]

    def spin():
        while not stop_flag[0]:
            sys.stdout.write(f"\r{message} {next(spinner)}")
            sys.stdout.flush()
            time.sleep(0.1)

    t = threading.Thread(target=spin)
    t.start()
    return lambda: stop_flag.__setitem__(0, True)