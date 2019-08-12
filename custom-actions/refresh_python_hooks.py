folderName = "Apps"
actionName = "Refresh Python Hooks"
import flame
import random
from time import gmtime, strftime
# from pynput.keyboard import *
from pynput.keyboard import *
import time
def mainWindow(selection):
    time_stamp = strftime("%H:%M:%S", gmtime())
    random_number = ''.join(random.choice('123456789') for i in range(2))
    random_number = int(random_number)
    keyboard = Controller()
    flame.execute_shortcut("Rescan Python Hooks")
    keyboard.press(Key.alt)
    keyboard.press(Key.tab)
    keyboard.release(Key.alt)
    keyboard.release(Key.tab)
    print "*" * random_number
    time.sleep(0.5)
    print time_stamp
    random_number = ''.join(random.choice('123456789') for i in range(1))
    random_number = int(random_number)
    print "*" * random_number * random_number
    return ()
def get_main_menu_custom_ui_actions():
    return [{'name': folderName,'actions': [{'name': actionName,'execute': mainWindow}]}]

#########################
"""
Created By: John Fegan
Description:
Rescans Python Hooks, and prints 10 * in the shell

Creation Date: 05.01.19
Updates:
06.11.19 - added folderName/actionName variable. Added comment section. Added keyboard shortcut to navigate to the shell.
06.26.19 - 1. added random number variable to print a different amount * each time python hooks have been scanned. 2. added time stamp variable, the script now prints a time stamp in the shell to show when it was last updated. 3. Added the script to the "Apps" folder in the main menu.

Keyboard Shortcut:
MacAir: Ctrl + Shift + R
"""
