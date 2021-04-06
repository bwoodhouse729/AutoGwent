# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:39:03 2021

@author: bwoodhouse

Maintain game state while playing Gwent and take automatic actions.

Settings: 
Resolution 1600 x 900, game window in upper-left of screen.
Graphics -> Premium Cards -> Disabled

Initial goals:
Automatically play a game.
Random mulligan, random plays (of trivial deck to play).
Pass if opponent passes and you are ahead in score, otherwise play to random location.

TODO: Take a few screenshots of each type of screen for development purposes.
"""

import cv2
from glob import glob
import imagehash
import imageio
from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
import pickle
from PIL import Image
import pyautogui
from sklearn import tree
import time

def analyze_game_state():
    # observe and record everything possible about the current game state
    
    take_screenshot()
    
    # Identify the current game window
    board_active = check_for_board()
    card_choice_active = check_for_card_choice()
    mulligans_active = check_for_mulligan()
    
    if board_active:
        # TODO: Identify opponent faction
        # TODO: Identify opponent leader ability
        # TODO: Identify number of leader ability charges remaining
        # TODO: Identify current player
        # TODO: Identify if opponent has passed
        # TODO: Identify current scores
        # TODO: Identify cards on each row of the board via their image/video
        # TODO: Identify card power
        # TODO: Identify card armor
        # TODO: Identify card statuses
        # TODO: Identify if card is premium or regular version
        # TODO: Identify presence of order ability
        # TODO: Identify order ability status (gray, red, or green)
        # TODO: Identify number of order charges
        # TODO: Identify cards in (my) hand
        # TODO: Identify card power/armor/status in my hand
        # TODO: Identify number of cards in each player's hand
        pass
    
    if mulligans_active:
        # TODO: Identify number of mulligans available
        # TODO: Identify cards to choose from
        pass
    
    if card_choice_active:
        # TODO: Identify the cards available to choose from
        # TODO: Identify the number of choices to be made
        pass
    
    # TODO: If opponent is playing a card, record it
    # Recognizing more detailed opponent actions would be quite tricky (and not that helpful?)

def check_for_board():
    # return True if currently viewing the game board
    pass

def check_for_card_choice():
    # return True if currently making a choice between cards
    pass

def check_for_game_select():
    # return True if currently on the game select screen
    pass

def check_for_mulligan():
    # return True if currently viewing a mulligan pane
    pass

def end_game():
    # click in a few places to move back to primary menu
    pass

def image_hash(width, height, image):
    fraction_x = 0.2
    fraction_y = 0.25
    image = image[int(image.shape[0] * fraction_x):-int(image.shape[0] * fraction_x), int(image.shape[1] * fraction_y):-int(image.shape[1] * fraction_y)]
    
    # resize image
    image = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)
    
    im = Image.fromarray(image)
    active_hash = imagehash.average_hash(im)
    return active_hash

def image_hash_reference():
    files = glob('./card_images_no_tooltip/*')
    names = []
    hashes = []
    for i in range(len(files)):
        #print(i)
        file = files[i]
        name = file.split('\\')[-1][:-4]
        names.append(name)
        #print(name)
        image = cv2.imread(file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        fraction_x = 0.2
        fraction_y = 0.25
        image = image[int(image.shape[0] * fraction_x):-int(image.shape[0] * fraction_x), int(image.shape[1] * fraction_y):-int(image.shape[1] * fraction_y)]
        
        scale_percent = 50 # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
          
        # resize image
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        
        # plt.imshow(image)
        # plt.show()
        
        # print()
        # print()
        
        im = Image.fromarray(image)
        active_hash = imagehash.average_hash(im)
        hashes.append(active_hash)
        
    return width, height, names, hashes

def initialize_game():
    # click to launch a game, then wait until game starts
    # TODO: click to launch a game
    # TODO: wait until mulligan screen
    pass

def make_move():
    # follow a specified behavior pattern and click appropriately to play a card
    
    # TODO: Initially, play a random card and end turn
    
    # Potential actions:
    # End turn
    # Pass
    # Play a card in a specific position
    # Activate card order
    # Target unit(s)
    # Choose card(s) from card choice screen
    # Mulligan
    # Return from targeting mode
    
    pass

def make_mulligans(width, height, names, hashes):
    # identify and click cards for mulligan
    
    # Load test image
    image = cv2.imread('./development_screenshots/sample_start_of_game.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # plt.imshow(image)
    # plt.show()
    
    # TODO: Identify number of mulligans remaining (1 - 5)
    
    # Use edge detection to isolate cards
    cards = []
    
    edges = cv2.Canny(image,100,200)
    # plt.imshow(edges, cmap='gray')
    # plt.show()
    
    # sum columns 450 to 1500 from rows 200 to 400, look for sums of 0
    subimage = edges[176:436, 450:1500]
    # plt.imshow(subimage, cmap='gray')
    # plt.show()
    sums = np.sum(subimage, axis=0)
    bools = sums > 300
    #print(sums > 0)
    
    # identify number of cards and bounding boxes of cards
    starts = []
    ends = []
    for i in range(1, len(bools)):
        if bools[i] and (not bools[i - 1]):
            starts.append(450 + i)
            # print(450 + i)
        elif (not bools[i]) and bools[i - 1]:
            ends.append(450 + i)
            # print(450 + i)
            
    for i in range(len(starts)):
        cards.append(image[176:436, starts[i]:ends[i]])
    
    # sum columns 450 to 1500 from rows 500 to 700, look for sums of 0
    subimage = edges[464:724, 450:1500]
    # plt.imshow(subimage, cmap='gray')
    # plt.show()
    sums = np.sum(subimage, axis=0)
    bools = sums > 300
    #print(sums > 0)
    
    # identify number of cards and bounding boxes of cards
    starts = []
    ends = []
    for i in range(1, len(bools)):
        if bools[i] and (not bools[i - 1]):
            starts.append(450 + i)
        elif (not bools[i]) and bools[i - 1]:
            ends.append(450 + i)
            
    for i in range(len(starts)):
        cards.append(image[464:724, starts[i]:ends[i]])
    
    # TODO: Make sure saved images are up-to-date for all cards
    # Add Way of the Witcher and 12 new leaders if necessary
    
    # TODO: Identify cards by comparing to saved images
    for card in cards:
        plt.imshow(card)
        plt.show()
        #print(np.shape(card))
        active_hash = image_hash(width, height, card)
        
        min_distance = 1000000000
        best_match = ''
        for i in range(len(hashes)):
            current_hash = hashes[i]
            distance = abs(active_hash - current_hash)
            if distance < min_distance:
                min_distance = distance
                best_match = names[i]
        print(best_match)
    
    # Special processing required for shield effect
    
    # TODO: Select card to mulligan at this point
    
    # TODO: Click on selected card
    # Requires storing the coordinates of the center of each card
    
    pass

def classify(clf, width, height, names, image):
    # image = cv2.imread(path)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    fraction_x = 0.2
    fraction_y = 0.25
    image = image[int(image.shape[0] * fraction_x):-int(image.shape[0] * fraction_x), int(image.shape[1] * fraction_y):-int(image.shape[1] * fraction_y)]
    
    image = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)

    plt.imshow(image)
    plt.show()

    index = clf.predict([np.ndarray.flatten(image)])[0]
    return names[index]

def take_screenshot():
    # Screenshot the whole game window and save it out
    myScreenshot = pyautogui.screenshot(region=(0, 31, 1600, 900))
    myScreenshot.save('./screenshots/active_screen.png')

def train_decision_tree():
    # Train a decision tree on middle portion of all test images
    files = glob('./card_images_no_tooltip/*')
    X = []
    Y = []
    names = []
    special_image = []
    for i in range(len(files)):
        print(i)
        file = files[i]
        name = file.split('\\')[-1][:-4]
        names.append(name)
        #print(name)
        image = cv2.imread(file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        fraction_x = 0.2
        fraction_y = 0.25
        image = image[int(image.shape[0] * fraction_x):-int(image.shape[0] * fraction_x), int(image.shape[1] * fraction_y):-int(image.shape[1] * fraction_y)]
        
        scale_percent = 50 # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
          
        # resize image
        image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        
        # if name == 'oneiromancy':
        #     plt.imshow(image)
        #     plt.show()
        
        # if i == 3:
        #     special_image = image
        
        # plt.imshow(image)
        # plt.show()
        
        # print()
        # print()
        
        X.append(np.ndarray.flatten(image))
        Y.append(i)
        
    # print(np.shape(X))
    # print(np.shape(Y))
    # print(Y)
    
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)
    
    # answer = clf.predict([np.ndarray.flatten(special_image)])
    # print(answer)
    
    return clf, width, height, names

def transition_game_select_play_standard():
    pyautogui.dragTo(378, 473, 0.1)
    pyautogui.click()
    
    # wait until game starts - look for mulligan screen
    # take screenshot every 2 seconds until pixel at (323, 405) is blue-green
    # blue-green is [48, 255, 255]
    attempts = 90
    threshold = 10
    for i in range(attempts):
        take_screenshot()
        image = imageio.imread('./screenshots/active_screen.png')
        
        # plt.imshow(image[320:330, 400:410])
        # plt.show()
        
        if (np.linalg.norm(image[323, 405] - [48, 255, 255]) < threshold):
            #print('found')
            break
        
        time.sleep(2)

def transition_home_game_select():
    pyautogui.dragTo(814, 472, 0.1)
    pyautogui.click()
    time.sleep(2)

if __name__ == "__main__":
    # recognize menu screen where a game can be launched
    # TODO: use check_for_game_select
    # play unranked for now
    
    # pause to allow user to make Gwent window active
    time.sleep(3)
    
    #take_screenshot()
    
    # transition_home_game_select()
    # transition_game_select_play_standard()
    
    # clf = pickle.load(open('./classifier.p', 'rb'))
    # width = pickle.load(open('./width.p', 'rb'))
    # height = pickle.load(open('./height.p', 'rb'))
    # names = pickle.load(open('./names.p', 'rb'))
    
    width, height, names, hashes = image_hash_reference()
    
    make_mulligans(width, height, names, hashes)
    
    # # start = time.time()
    # clf, width, height, names = train_decision_tree()
    # # end = time.time()
    # # print(int(end - start))
    # pickle.dump(clf, open('./classifier.p', 'wb'))
    # pickle.dump(width, open('./width.p', 'wb'))
    # pickle.dump(height, open('./height.p', 'wb'))
    # pickle.dump(names, open('./names.p', 'wb'))
    
    # name = classify(clf, width, height, names, './card_images_no_tooltip/adrenaline rush.png')
    # print(name)
    
    # image = imageio.imread('./development_screenshots/sample_start_of_game.png')
    # print(image[323, 405])
    
    
        
    
    # infinite loop to keep playing more games
    # while True:
    #     initialize_game()
    #     game_active = True
    #     my_turn = True
    #     while game_active:
    #         analyze_game_state()
    #         if my_turn:
    #             make_move()
    #             time.sleep(1)
                
    #         # for testing purposes
    #         game_active = False
    #     end_game()
    #     break