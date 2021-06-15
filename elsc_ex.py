import time
import random
import os
from psychopy import visual
import ctypes
from psychopy import event
from psychopy.hardware import keyboard
from psychopy import core
import csv

BLOCKS_CATEGORY = ['faces', 'cars', 'cars_scrambled', 'faces_scrambled']
FOLDERS_CATEGORY = ['faces', 'cars']
NUM_BLOCKS = 4
NUM_TRIALS = 40
PEEKED_PHOTOS = []


def creating_window():
    # checking the sizes of the screen
    user32 = ctypes.windll.user32
    width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    win = visual.Window((width, height))  # creating the window

    text_screen = visual.TextStim(win, "אני")  # creating a text on the screen
    # button = visual.ButtonStim(win,"start",pos=(0,0))
    text_screen.draw()
    win.flip()
    time.sleep(0.2)
    return win


def showing_photos():
    im = visual.ImageStim(win, "instructions.png", size=[2, 2])  # handling with the instructions
    im.draw()
    win.flip()
    event.waitKeys()  # wait for some button pressing

    for block in range(NUM_BLOCKS):
        block_choice = random.choice(BLOCKS_CATEGORY)  # peeking randomly category for block
        BLOCKS_CATEGORY.remove(block_choice)  # making sure that we won't peek the same category twice
        text_screen1 = visual.TextStim(
                                    win,
                                    "the category is:  " + block_choice,
                                    pos=(0, 0),
                                    color='white')  # creating a text on the screen
        button = visual.ButtonStim(
                                    win,
                                    "start",
                                    size=[0.1, 0.1],
                                    pos=(0, -0.3),
                                    color='red')
        button.draw()
        text_screen1.draw()
        win.flip()
        while not button.isClicked:  # continue only if the button pressed
            continue
        time.sleep(0.2)  # giving the user some extra time

        for trial in range(2):
            random_category = random.choice(FOLDERS_CATEGORY)  # peeking randomly category
            random_photo = random.choice(
                                        [x for x in os.listdir(random_category)
                                        if os.path.isfile(os.path.join(random_category, x))])
            while random_photo in PEEKED_PHOTOS:  # making sure that we won't choose the same photo twice
                random_photo = random.choice(
                    [x for x in os.listdir(random_category) if os.path.isfile(os.path.join(random_category, x))])
            PEEKED_PHOTOS.append(random_photo)
            image = visual.ImageStim(win, random_category + "/" + random_photo, size=[0.6, 0.9])
            image.draw()
            win.flip()
            time.sleep(0.4)
            button = visual.ButtonStim(
                                        win,
                                        text='',
                                        size=[0.05, 0.1],
                                        pos=(0, 0))
            button.draw()
            win.flip()
            user_result = event.getKeys(keyList=['space'], modifiers=False)
            time.sleep(0.6)

    # win.flip()
    # time.sleep(0.4)


if __name__ == '__main__':
    win = creating_window()
    showing_photos()
    win.close()
