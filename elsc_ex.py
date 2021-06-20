# LAB EXPERIMENT WRITTEN BY NATALI YOSUPOV
# DATE 20.06.2021

import time
import random
import os
import psychopy.clock
from psychopy import visual
import ctypes
from psychopy import event
import csv


BLOCKS_CATEGORY = ['faces', 'cars', 'cars_scrambled', 'faces_scrambled']
FOLDERS_CATEGORY = ['faces', 'cars', 'faces scrambled', 'cars scrambled']
DATA_TO_KNOW = ['block_number', 'target_category', 'trial_number', 'image_presented', 'present_ca_image',
                     'stimulus_duration', 'user_response', 'correct_response', 'response_time']
NUM_BLOCKS = 4
NUM_TRIALS = 40
PEEKED_PHOTOS = []


def creating_window():

    # checking the sizes of the screen
    user_screen = ctypes.windll.user32
    width, height = user_screen.GetSystemMetrics(0), user_screen.GetSystemMetrics(1)

    # creating the window
    win = visual.Window((width, height))
    win.flip()
    time.sleep(0.2)

    return win


def showing_photos(writer):

    block_number, trial_number = 0, 0
    prev_choice = None
    photo_dict = {}

    instruction_text = visual.TextStim(win, pos=(0, 0), text=INSTRUCTION_TEXT)  # handling with the instructions
    instruction_text.draw()
    win.flip()

    # wait for some button pressing
    event.waitKeys()

    #  initialize the names of all the images to a dict
    for category_folder in FOLDERS_CATEGORY:
        photo_dict[category_folder] = [x for x in os.listdir(category_folder) if os.path.isfile(os.path.join(category_folder, x))]

    for block in range(NUM_BLOCKS):
        # peeking randomly category for block
        target_category = random.choice(BLOCKS_CATEGORY)

        # making sure that we won't peek the same category twice
        BLOCKS_CATEGORY.remove(target_category)

        # the label that shows the category name
        text_start_block = visual.TextStim(win, "the category is:  " + target_category + "\n \n press space to start", pos=(0, 0), color='white')
        text_start_block.draw()
        win.flip()

        # continue the program only after the user pressed space
        event.waitKeys(keyList=['space'])

        # the fixation point
        fixation = psychopy.visual.DotStim(win, units='pix', dotLife=-1, dotSize=10)
        fixation.draw()
        win.flip()
        time.sleep(0.2)

        PEEKED_PHOTOS.clear()

        for trial in range(NUM_TRIALS):

            # peeking randomly category
            random_category = random.choice(FOLDERS_CATEGORY)

            # checking if the random choice is the target category for not having two photos from target category in a row
            # checking also if the prev photo is the same as now, if the answer is yes we want to choose other
            if random_category == target_category and prev_choice == random_category:

                # choose other category
                while prev_choice == random_category:
                    random_category = random.choice(FOLDERS_CATEGORY)

                # choose randomly image
                image_presented = random.choice(photo_dict[random_category])  # todo optimize ,define before loop,pick in loop

            elif random_category == target_category and prev_choice != random_category:

                # choose randomly image
                image_presented = random.choice(photo_dict[random_category])

                # making sure that we won't choose the same photo twice
                while image_presented in PEEKED_PHOTOS:
                    image_presented = random.choice(photo_dict[random_category])

                # after we make sure the image was not shown in the target category yet, the image is added to the list
                PEEKED_PHOTOS.append(image_presented)

            else:  # if the trail category is not the target category
                # choose random image
                image_presented = random.choice(photo_dict[random_category])

            # update the prev category
            prev_choice = random_category

            trail_clock = psychopy.clock.Clock()

            # representing the image
            image = visual.ImageStim(win, random_category + "/" + image_presented, size=[0.6, 0.9])
            image.draw()
            image_onset = win.flip()
            time.sleep(0.4)

            fixation.draw()
            image_drop_time = win.flip()

            # check the time the image was on the screen
            duration = image_drop_time - image_onset

            pressed = event.waitKeys(maxWait=1, keyList=['space'], timeStamped=psychopy.clock.Clock())

            # making sure that the fixation point will stay for 1 second, and not less
            time_to_sleep = (1-pressed[0][1]) if pressed else 0
            time.sleep(time_to_sleep)

            # checking if the user pressed 'space'
            if pressed is not None:

                # True if he pressed
                user_response = True
                response_time = pressed[0][1]
            else:
                # False if not
                user_response = False
                response_time = 0

            # checking if the photo is from the target category
            if target_category == random_category:
                correct_response = True  # True if yes
            else:
                correct_response = False  # False if not
            # time.sleep(0.6)

            writer.writerow([block_number, target_category, trial_number, image_presented, random_category, duration, user_response, correct_response, response_time])
            trial_number += 1

        trial_number = 0
        block_number += 1


if __name__ == '__main__':
    win = creating_window()
    results_file = open('results.csv', 'w', newline='')
    writer = csv.writer(results_file)

    f = open("instructions.txt", "r")
    INSTRUCTION_TEXT = f.read()

    writer.writerow(DATA_TO_KNOW)
    showing_photos(writer)
    results_file.close()
    win.close()
