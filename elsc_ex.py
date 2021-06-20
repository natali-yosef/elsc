import time
import random
import os

import psychopy.clock
from psychopy import visual
import ctypes
from psychopy import event
from psychopy.hardware import keyboard
from psychopy import core
import csv


BLOCKS_CATEGORY = ['faces', 'cars', 'cars_scrambled', 'faces_scrambled']
FOLDERS_CATEGORY = ['faces', 'cars', 'faces scrambled', 'cars scrambled']
NUM_BLOCKS = 4
# NUM_TRIALS = 40
NUM_TRIALS = 5
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
    prev_choice = None
    photo_dict = {}
    instruction_text = visual.TextStim(win, pos=(0, 0), text=INSTRUCTION_TEXT)  # handling with the instructions
    instruction_text.draw()
    win.flip()
    event.waitKeys()  # wait for some button pressing

    #  initialize the names of all the images to a dict
    for category_folder in FOLDERS_CATEGORY:
        photo_dict[category_folder] = [x for x in os.listdir(category_folder) if os.path.isfile(os.path.join(category_folder, x))]


    # todo log onset time:when did we saw the picture on screen, offset time: time between last flip and new onset
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
                # choose randomly image
                image_presented = random.choice(photo_dict[random_category])

            # update the prev category
            prev_choice = random_category

            trail_clock = psychopy.clock.Clock()

            # representing the image
            image = visual.ImageStim(win, random_category + "/" + image_presented, size=[0.6, 0.9])
            image.draw()
            # stim_onset = win.flip()
            win.flip()
            time.sleep(0.4)
            image_drop_time = fixation.draw()
            # duration = stim_onset-image_drop_time
            win.flip()
            # key_list = event.getKeys(keyList=['space'], modifiers=False)
            pressed = event.waitKeys(maxWait=1, keyList=['space'], timeStamped=psychopy.clock.Clock())
            time_to_sleep = 1-pressed[0][1] if pressed else 0
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

            writer.writerow([block_number, target_category, trial_number, image_presented, random_category, STIMULUS_DURATION, user_response, correct_response, response_time])
            trial_number += 1
        trial_number = 0
        block_number += 1


if __name__ == '__main__':
    win = creating_window()
    results_file = open('results.csv', 'w', newline='')
    writer = csv.writer(results_file)

    f = open("instructions.txt", "r")
    INSTRUCTION_TEXT = f.read()

    writer.writerow(['block_number', 'target_category', 'trial_number', 'image_presented', 'present_ca_image',
                     'stimulus_duration', 'user_response', 'correct_response', 'response_time'])
    showing_photos(writer)
    results_file.close()
    win.close()
