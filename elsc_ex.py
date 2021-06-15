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
# NUM_TRIALS = 40
NUM_TRIALS = 2
STIMULUS_DURATION = 400  # how long was the picture shown on screen in milliseconds
PEEKED_PHOTOS = []


def creating_window():
    # checking the sizes of the screen
    user32 = ctypes.windll.user32
    width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    win = visual.Window((width, height))  # creating the window
    win.flip()
    time.sleep(0.2)
    return win


def showing_photos(writer):
    block_number, trial_number = 0, 0
    im = visual.ImageStim(win, "instructions.png", size=[2, 2])  # handling with the instructions
    im.draw()
    win.flip()
    event.waitKeys()  # wait for some button pressing

    for block in range(NUM_BLOCKS):
        target_category = random.choice(BLOCKS_CATEGORY)  # peeking randomly category for block
        BLOCKS_CATEGORY.remove(target_category)  # making sure that we won't peek the same category twice
        text_screen1 = visual.TextStim(
            win,
            "the category is:  " + target_category,
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

        for trial in range(NUM_TRIALS):
            random_category = random.choice(FOLDERS_CATEGORY)  # peeking randomly category
            image_presented = random.choice(
                [x for x in os.listdir(random_category)
                 if os.path.isfile(os.path.join(random_category, x))])
            while image_presented in PEEKED_PHOTOS:  # making sure that we won't choose the same photo twice
                image_presented = random.choice(
                    [x for x in os.listdir(random_category) if os.path.isfile(os.path.join(random_category, x))])
            PEEKED_PHOTOS.append(image_presented)
            image = visual.ImageStim(win, random_category + "/" + image_presented, size=[0.6, 0.9])
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
            key_list = event.getKeys(keyList=['space'], modifiers=False)
            if 'space' in key_list:  # checking if the user pressed 'space'
                user_response = True  # True if he pressed
            else:
                user_response = False  # False if not
            if target_category == random_category:  # checking if the photo is from the target category
                correct_response = True  # True if yes
            else:
                correct_response = False  # False if not
            time.sleep(0.6)
            response_time = 0
            writer.writerow(
                [block_number, target_category, trial_number, image_presented, random_category, STIMULUS_DURATION,
                 user_response, correct_response, response_time])
            # with results_file:
            #     writer = csv.writer(results_file)
            #     writer.writerow(
            #         [block_number, target_category, trial_number, image_presented, random_category, STIMULUS_DURATION,
            #          user_response, correct_response, response_time])
            trial_number += 1
        trial_number = 0
        block_number += 1
    # win.flip()
    # time.sleep(0.4)


if __name__ == '__main__':
    win = creating_window()
    results_file = open('results.csv', 'w', newline='')
    writer = csv.writer(results_file)
    writer.writerow(['block_number', 'target_category', 'trial_number', 'image_presented', 'present_ca_image',
                     'stimulus_duration', 'user_response', 'correct_response', 'response_time'])
    showing_photos(writer)
    results_file.close()
    win.close()
