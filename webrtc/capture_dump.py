import pyautogui
import sys
import time
from datetime import datetime

def get_mouse_position():
    try:
        while True:
            x, y = pyautogui.position()
            position_str = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(position_str, end='')
            print('\b' * len(position_str), end='', flush=True)
    except KeyboardInterrupt:
        print('\nDone.')

def click_specific_point(x, y):
    pyautogui.click(x, y)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py button_x button_y")
        sys.exit(1)
    
    interval = int(sys.argv[1])

    click_specific_point(113, 199)

    start_time = time.time()
    try:
        while True:
            click_specific_point(113, 199)
            time.sleep(interval * 60)
    except KeyboardInterrupt:
        end_time = time.time()
        duration_str = "Collected from " + str(datetime.fromtimestamp(start_time)) + \
            " to " + str(datetime.fromtimestamp(end_time))
        print(duration_str + "\nDone.")

