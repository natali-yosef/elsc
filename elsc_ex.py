# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

import random

import os
from psychopy import visual

import ctypes

user32 = ctypes.windll.user32
Width, Height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

win = visual.Window((Width, Height))

# text_screen = visual.TextStim(win,"text3")
# button = visual.ButtonStim(win,"start",pos=(0,0))

foo = ['faces', 'cars']

random_choice = random.choice(foo)
path = r"C:\Users\נטלי\PycharmProjects\pythonProject1"+"/"+random_choice
random_filename = random.choice([x for x in os.listdir(path)
                                 if os.path.isfile(os.path.join(path, x))])

image = visual.ImageStim(win, random_choice+ "/"+random_filename)


# text_screen.draw()
win.flip()
time.sleep(3)
image.draw()
win.flip()
time.sleep(3)



