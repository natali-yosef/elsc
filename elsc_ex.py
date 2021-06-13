import time
import random
import os
from psychopy import visual
import ctypes

BLOCKS_CATEGORY = ['faces', 'cars', 'cars_scrambled', 'faces_scrambled']
FOLDERS_CATEGORY = ['faces', 'cars']
NUM_BLOCKS = 4
NUM_TRIALS = 40
PEEKED_PHOTOS = []

# checking the sizes of the screen
user32 = ctypes.windll.user32
Width, Height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

win = visual.Window((Width, Height))  # creating the window

text_screen = visual.TextStim(win, "אני")  # creating a text on the screen
# button = visual.ButtonStim(win,"start",pos=(0,0))
text_screen.draw()
win.flip()
time.sleep(0.2)


for block in range(NUM_BLOCKS):  #
    block_choice = random.choice(BLOCKS_CATEGORY)  # peeking randomly category for block
    BLOCKS_CATEGORY.remove(block_choice)  # making sure that we won't peek same category twice

    for trial in range(NUM_TRIALS):
        random_category = random.choice(FOLDERS_CATEGORY)  # peeking randomly category
        random_photo = random.choice(
            [x for x in os.listdir(random_category) if os.path.isfile(os.path.join(random_category, x))])
        while random_photo in PEEKED_PHOTOS:  # making sure that we won't choose the same photo twice
            random_photo = random.choice(
                [x for x in os.listdir(random_category) if os.path.isfile(os.path.join(random_category, x))])
        PEEKED_PHOTOS.append(random_photo)
        image = visual.ImageStim(win, random_category + "/" + random_photo)
        image.draw()
        win.flip()
        time.sleep(0.4)


win.flip()
time.sleep(0.4)


