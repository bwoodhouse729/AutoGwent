# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:39:03 2021

@author: bwoodhouse

Maintain game state while playing Gwent and take automatic actions.

Settings: 
Only supports play on PC
Resolution 1600 x 900, game window in upper-left of screen.
Graphics -> Premium Cards -> Disabled

Initial goals:
Automatically play a game with simple card plays and random choices.
Random mulligan, random plays (of trivial deck to play).
Pass if opponent passes and you are ahead in score, otherwise play to random location.

If possible, avoid using text besides numbers.  Other languages will cause issues.
TODO: Take a few screenshots of each type of screen for development purposes.
TODO: Fill out skeleton by developing routines to recognize various aspects of the game.
TODO: Long-term, connect with C++ game simulator and AI engine to make choices
      This script will execute the choices made.
TODO: Log each game in an easy-to-process manner.
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

class Card:
    def Card(self, name):
        self.name = name
        
        self.power = -1
        self.armor = -1
        
        # statuses
        self.vitality_bleed = 0
        self.defender = False
        self.doomed = False
        self.immunity = False
        self.locked = False
        self.poisoned = False
        self.resilience = False
        self.rupture = False
        self.shield = False
        self.spying = False
        self.veil = False
        
    def set_power(self, power):
        self.power = power
    
    def set_armor(self, armor):
        self.armor = armor
        
    def add_vitality(self, amount):
        self.vitality_bleed += amount
        
    def add_bleed(self, amount):
        self.vitality_bleed -= amount
        
    def add_defender(self):
        self.defender = True
        
    def add_doomed(self):
        self.doomed = True
        
    def add_immunity(self):
        self.immunity = True
        
    def add_locked(self):
        self.locked = True
        
    def add_poisoned(self):
        self.poisoned = True
        
    def add_resilience(self):
        self.resilience = True
        
    def add_rupture(self):
        self.rupture = True
        
    def add_shield(self):
        self.shield = True
        
    def add_spying(self):
        self.spying = True
        
    def add_veil(self):
        self.veil = True

# TODO: update width and height for various types of card images
width = 0
height = 0
ref_names = []
ref_hashes = []

mulligan_names = []
mulligan_centers = []
number_of_mulligans = 0

card_choice_names = []
card_choice_centers = []
card_choice_count = 0

board_active = False
card_choice_active = False
game_select_active = False
home_active = False
mulligans_active = False

current_player = -1 # 0 is allied turn, 1 is enemy turn
enemy_cards_played = []
enemy_faction = ''
enemy_leader_ability = ''
enemy_leader_ability_charges = -1
enemy_passed = False
scores = [0, 0]
board = [[], [], [], []] # rows from bottom-up, contains Cards
allied_hand = []
number_of_enemy_cards = -1

def action_end_targeting():
    # right click? to end targeting mode
    pass

def action_end_turn():
    # click button to end turn
    pyautogui.dragTo(1539, 480, 0.1)
    pyautogui.click()

def action_order_card(row, position):
    # execute order on card in specified row and position
    pass

def action_hard_pass():
    # click and hold end turn button to hard pass
    pyautogui.dragTo(1539, 480, 0.1)
    pyautogui.mouseDown()
    time.sleep(1)
    pyautogui.mouseUp()
    
def action_play_card(index, row, position):
    # play card from hand in position index
    pass

def action_target_card(row, position):
    # click card in specified row and position to assign target of action
    pass

def analyze_game_state():
    # observe and record everything possible about the current game state
    
    take_screenshot()
    
    # Identify the current game window
    home_active = check_for_home()
    if home_active:
        game_select_active = False
        board_active = False
        card_choice_active = False
        mulligans_active = False
    else:
        game_select_active = check_for_game_select()
        if game_select_active:
            board_active = False
            card_choice_active = False
            mulligans_active = False
        else:
            board_active = check_for_board()
            if board_active:
                card_choice_active = False
                mulligans_active = False
            else:
                mulligans_active = check_for_mulligan()
                if mulligans_active:
                    card_choice_active = False
                else:
                    # default to card_choice_active
                    card_choice_active = True
    if home_active:
        pass # nothing to do
    elif game_select_active:
        pass # nothing to do
    elif board_active:
        current_player = identify_current_player()
        if current_player == 1:
            # if opponent is playing a card, record it
            enemy_card = identify_opponent_card()
            if enemy_card != '':
                enemy_cards_played.append(enemy_card)
        else:
            enemy_faction, enemy_leader_ability, enemy_leader_ability_charges = identify_enemy_leader_ability()
            enemy_passed = identify_enemy_passed()
            scores = identify_scores()
            board = identify_board()
            allied_hand = identify_allied_hand()
            number_of_enemy_cards = identify_number_of_enemy_cards()
    elif mulligans_active:
        number_of_mulligans = identify_number_of_mulligans()
        mulligan_names, mulligan_centers = identify_mulligan_choices()
    elif card_choice_active:
        card_choice_names, card_choice_centers = identify_card_choices()
        card_choice_count = identify_choice_count()

def check_for_board():
    # return True if currently viewing the game board
    pass

def check_for_card_choice():
    # return True if currently making a choice between cards
    pass

def check_for_game_select():
    # return True if currently on the game select screen
    pass

def check_for_home():
    # return True if currently on the home screen
    pass

def check_for_mulligan():
    # return True if currently viewing a mulligan screen
    take_screenshot()
    image = imageio.imread('./screenshots/active_screen.png')
    
    # plt.imshow(image[320:330, 400:410])
    # plt.show()
    
    threshold = 10
    if (np.linalg.norm(image[323, 405] - [48, 255, 255]) < threshold):
        return True
    else:
        return False

def choose_mulligan():
    options = mulligan_names
    # identify which card to mulligan from a list of cards
    # choice can be based on number_of_mulligans
    # TODO: continue should also be a choice
    return 0

def end_game():
    # click in a few places to move back to primary menu
    pass

def identify_allied_hand():
    # Identify all cards in my hand, with their power/armor/icon status
    pass

def identify_board():
    # Identify all cards on the board and their various attributes
    # TODO: Identify cards on each row of the board via their static image
    # Start by using lower right corner of the cards (bronze or gold) to
    # indicate how many cards are present.  Need coordinates for even & odd
    # (take photos of 8 and 9 card rows), all 4 corners.
    
    # TODO: Recognize the back of cards as well for traps
    # TODO: Identify card power
    # TODO: Identify card armor
    # TODO: Identify card statuses
    # TODO: Identify presence of card order ability
    # TODO: Identify order ability status (gray, red, or green) if present
    # TODO: Identify number of order charges if present
    pass

def identify_card_choices():
    # identify cards to choose from in choice screen
    # TODO: In a few rare cases, may have to read tooltip
    pass

def identify_choice_count():
    # when selecting cards, identify how many cards to choose
    pass

def identify_current_player():
    # use coin image to identify current player
    pass

def identify_enemy_leader_ability():
    # use leader ability image to identify enemy leader ability
    # return faction, leader_ability, charges
    pass

def identify_enemy_passed():
    # identify if the enemy has passed
    pass

def identify_number_of_enemy_cards():
    # identify the number of cards in the enemy's hand
    pass

def identify_opponent_card():
    # check if enemy is playing a card
    # if they are, recognize it from the image
    # return card name
    # if not, return ''
    pass

def identify_mulligan_choices(width, height, names, hashes):
    # identify and click cards for mulligan
    
    # Load test image
    image = cv2.imread('./development_screenshots/sample_start_of_game.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # plt.imshow(image)
    # plt.show()
    
    # Use edge detection to isolate cards
    cards = []
    centers = []
    
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
        centers.append([250, int(0.5 * (starts[i] + ends[i]))])
    
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
    
    names = []
    for card in cards:
        # plt.imshow(card)
        # plt.show()
        # print(np.shape(card))
        
        active_hash = image_hash(width, height, card)
        
        min_distance = 1000000000
        best_match = ''
        for i in range(len(hashes)):
            current_hash = hashes[i]
            distance = abs(active_hash - current_hash)
            if distance < min_distance:
                min_distance = distance
                best_match = names[i]
        names.append(best_match)
    
    return names, centers

def identify_number_of_mulligans():
    # on the mulligan screen, identify number of mulligans to be made
    # TODO: Use custom imagehash classifier for a screenshot of digits 1 - 5
    pass

def identify_scores():
    # identify total scores on the righthand side of the board
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

def make_card_choice():
    # Select card(s) from card choice screen
    # Hit continue when done
    pass

def make_move():
    # click appropriately to make a move in active game
    
    if game_select_active:
        transition_game_select_play_standard()
    elif mulligans_active:
        make_mulligan(mulligan_names, mulligan_centers)
    elif card_choice_active:
        make_card_choice()
    elif board_active:
        # Make 1 action based on current board state
        
        # Potential actions:
        # action_end_turn
        # action_pass
        # action_play_card(index)
        # action_order_card(row, position)
        # action_target_card(row, position)
        # action_end_targeting()
        
        # TODO: Initially, play a random card and end turn
        pass

def make_mulligan():
    # Select card to mulligan at this point
    index = choose_mulligan()
    
    # Click on selected card
    pyautogui.dragTo(mulligan_centers[index][0], mulligan_centers[index][1], 0.1)
    pyautogui.click()

def take_screenshot():
    # Screenshot the whole game window and save it out
    myScreenshot = pyautogui.screenshot(region=(0, 31, 1600, 900))
    myScreenshot.save('./screenshots/active_screen.png')

def transition_game_select_play_standard():
    # click to play a standard game, then wait for mulligan screen
    
    pyautogui.dragTo(378, 473, 0.1)
    pyautogui.click()
    
    # wait until first action - look for mulligan screen
    # take screenshot every 2 seconds until pixel at (323, 405) is blue-green
    # blue-green is [48, 255, 255]
    attempts = 90
    for i in range(attempts):
        result = check_for_mulligan()
        
        if result:
            break
        
        time.sleep(2)

def transition_home_game_select():
    pyautogui.dragTo(814, 472, 0.1)
    pyautogui.click()
    time.sleep(2)

if __name__ == "__main__":
    
    # pause to allow user to make Gwent window active
    time.sleep(3)
    
    # uncomment to take screenshot for development
    take_screenshot()
    
    # uncomment to create image hash references based on image library of cards
    # width, height, names, hashes = image_hash_reference()
    # pickle.dump(width, open('./classifier/width.p', 'wb'))
    # pickle.dump(height, open('./classifier/height.p', 'wb'))
    # pickle.dump(names, open('./classifier/names.p', 'wb'))
    # pickle.dump(hashes, open('./classifier/hashes.p', 'wb'))
    
    # load classifier parameters from files
    width = pickle.load(open('./classifier/width.p', 'rb'))
    height = pickle.load(open('./classifier/height.p', 'rb'))
    ref_names = pickle.load(open('./classifier/names.p', 'rb'))
    ref_hashes = pickle.load(open('./classifier/hashes.p', 'rb'))
    
    #action_hard_pass()
    
    # analyze_game_state()
    # make_move()
    
    # # start = time.time()
    # clf, width, height, names = train_decision_tree()
    # # end = time.time()
    # # print(int(end - start))
    # pickle.dump(clf, open('./classifier.p', 'wb'))
    # pickle.dump(width, open('./width.p', 'wb'))
    # pickle.dump(height, open('./height.p', 'wb'))
    # pickle.dump(names, open('./names.p', 'wb'))
    
    # infinite loop to keep playing more games
    # while True:
    #     analyze_game_state()
    #     make_move()
    #     time.sleep(1)