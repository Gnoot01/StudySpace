"""
Project Idea: https://elgoog.im/t-rex/
Check if works with greater speeds by Inspect Element>Console>"Runner.instance_.setSpeed=50"

'pip install pyautogui' + 'pip install pillow, but import PIL'
PyAutoGUI is all-rounded - can control the mouse, keyboard and perform basic image recognition (PIL)/faster advanced computer vision (OpenCV)
Selenium for anything web browser-based
Pyautogui for anything outside of browser (web extensions?/app)

Hard to use mouse to close program if mouse cursor moving around by itself, so fail-safe feature:
Default pyautogui.FAILSAFE = True, pyautogui.PAUSE = 0.1 gives 0.1s pause after each call, to move mouse into corner to raise pyautogui.FailSafeException & stop
"""
import pyautogui
from PIL import Image, ImageGrab
import keyboard
import time


def click(key):
    pyautogui.press(key)
    return


def isCollision(data):
    for x in range(75, 160):
        for y in range(95, 125):
            if data[x, y] < 100:
                click("up")
                return
    # Check collision for birds
    for x in range(70, 100):
        for y in range(65, 90):
            if data[x, y] < 171:
                click("down")
                return
    # # coords provided are relative to screen. bbox reduces screen size, to locate in smaller region & faster
    # # without bbox:
    #     # Check collision for cactus
    #     for x in range(735, 830):
    #         for y in range(395, 425):
    #             if data[x, y] < 100:
    #                 click("up")
    #                 return
    #     # Check collision for birds
    #     for x in range(730, 760):
    #         for y in range(365, 390):
    #             if data[x, y] < 171:
    #                 click("down")
    #                 return
    return


time.sleep(2) # for some time to get to screen
click('up')

# press q to stop script
while not keyboard.is_pressed("q"):
    # "RGB/L(greyscale for image processing)"
    image = ImageGrab.grab(bbox=(660, 300, 1275, 450)).convert('L')
    data = image.load()
    isCollision(data)

    # # Debugging
    # # Display rectangle box for cactus
    # # ^x->right, ^y->lower
    # for x in range(735, 830):
    #     for y in range(395, 425):
    #          # colors the box
    #          data[x, y] = 100
    #
    # # Display rectangle box for birds
    # for x in range(730, 760):
    #     for y in range(365, 390):
    #         data[x, y] = 171
    #
    # image.show()
    # break
