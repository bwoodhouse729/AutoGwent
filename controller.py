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

def classify_card_image(card):
    
    # TODO: Improve classifications by using faction information from csv
    
    active_hash = image_hash(width, height, card)
        
    min_distance = 1000000000
    best_match = ''
    for i in range(len(ref_hashes)):
        current_hash = ref_hashes[i]
        distance = abs(active_hash - current_hash)
        if distance < min_distance:
            min_distance = distance
            best_match = ref_names[i]
    
    return best_match

def end_game():
    # click in a few places to move back to primary menu
    pass

def identify_allied_hand():
    # Identify all cards in my hand, with their power/armor/icon status
    pass

def identify_board():
    # Identify all cards on the board and their various attributes
    # Note the coordinates depend on whose turn it is.  The camera zooms
    # out when it is player 0's turn.
    
    # Use cluster in upper left of card to identify card presence
    # Use left-most diamond as an indication of how many cards to expect
    
    # TODO: Could restrict to units and artifacts for classification here
    
    #image = cv2.imread('./development_screenshots/sample_board_9_cards.png')
    image = cv2.imread('./development_screenshots/sample_read_board.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    diamond_heights = [134, 267, 422, 589]
    left_starts = [363, 345, 335, 294]
    card_starts = [363, 345, 315, 294]
    widths = [95, 102, 108, 113]
    
    # coordinates of cards, by row
    upper_lefts_odd = [[[121, 367], [121, 463], [121, 560], [121, 658], [121, 754], [121, 851], [121, 948], [121, 1045], [121, 1142]],
                        [[252, 347], [252, 449], [252, 550], [252, 652], [252, 753], [252, 855], [252, 957], [252, 1058], [252, 1159]],
                        [[406, 322], [406, 429], [406, 535], [406, 642], [406, 750], [406, 857], [406, 964], [406, 1070], [406, 1178]],
                        [[570, 295], [570, 409], [570, 522], [570, 634], [570, 747], [570, 860], [570, 973], [570, 1085], [570, 1199]]]
    upper_rights_odd = [[[121, 458], [121, 555], [121, 653], [121, 749], [121, 846], [121, 943], [121, 1040], [121, 1137], [121, 1233]],
                        [[252, 444], [252, 545], [252, 647], [252, 748], [252, 850], [252, 952], [252, 1053], [252, 1154], [252, 1253]],
                        [[406, 422], [406, 530], [406, 637], [406, 745], [406, 852], [406, 958], [406, 1065], [406, 1172], [406, 1279]],
                        [[570, 403], [570, 516], [570, 627], [570, 741], [570, 854], [570, 967], [570, 1079], [570, 1191], [570, 1305]]]
    lower_lefts_odd = [[[253, 349], [253, 450], [239, 551], [239, 652], [239, 753], [239, 853], [239, 955], [239, 1055], [239, 1156]],
                        [[384, 326], [384, 432], [384, 538], [384, 644], [384, 750], [384, 856], [384, 962], [384, 1068], [384, 1174]],
                        [[554, 298], [554, 411], [554, 523], [554, 635], [554, 747], [554, 859], [554, 971], [554, 1083], [554, 1195]],
                        [[733, 270], [733, 389], [733, 507], [733, 625], [733, 744], [733, 861], [733, 980], [733, 1099], [733, 1218]]]
    lower_rights_odd = [[[239, 444], [239, 546], [239, 647], [239, 748], [239, 848], [239, 950], [239, 1050], [239, 1151], [239, 1252]],
                        [[384, 425], [384, 533], [384, 639], [384, 745], [384, 851], [384, 957], [384, 1063], [384, 1169], [384, 1275]],
                        [[554, 404], [554, 517], [554, 629], [554, 741], [554, 853], [554, 966], [554, 1077], [554, 1189], [554, 1301]],
                        [[733, 382], [733, 501], [733, 620], [733, 739], [733, 856], [733, 975], [733, 1093], [733, 1211], [733, 1330]]]
    upper_lefts_even = [[, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ],
                        [, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ],
                        [, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ],
                        [, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ]]
    upper_rights_even = [[, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ],
                          [, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ],
                          [, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ],
                          [, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ]]
    lower_lefts_even = [[, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ],
                        [, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ],
                        [, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ],
                        [, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ]]
    lower_rights_even = [[, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ],
                          [, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ],
                          [, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ],
                          [, ], [, ], [, ], [, ], [, ], [, ], [, ], [, ]]
    
    for row in range(4):
        
        estimated_count = 0
        
        hsv_image = cv2.cvtColor(image[diamond_heights[row] - 15:diamond_heights[row] + 15, left_starts[row]:left_starts[row] + 500], cv2.COLOR_RGB2HSV)
        lower = np.array([12, 50, 50])
        upper = np.array([30, 150, 150])
        mask = cv2.inRange(hsv_image, lower, upper)
        # plt.figure(figsize=(20, 20))
        # plt.imshow(mask)
        # plt.show()
        
        for i in range(0, np.shape(hsv_image)[1]):
            active_sum = sum(mask[:, i])
            if active_sum > 5 * 255:
                #print(i)
                estimated_count = int(round(9 - 2 * i / widths[row]))
                #print(estimated_count)
                break
        
        # TODO: Recover all cards based on estimated count, then identify them
        if estimated_count % 2 == 0 and estimated_count > 0:
            # start from coordinates of all 8 cards, pick out center ones appropriately
            start = 4.0 - (estimated_count / 2)
            for i in range(estimated_count):
                #card = image[upper_lefts_even[row][start + i][0]:lower_rights_even[row][start + i][0], upper_lefts_even[row][start + i][1]:lower_rights_even[row][start + i][1], :]
                # plt.imshow(card)
                # plt.show()
                pass
        else: # estimated_count % 2 == 1
            # start from coordinates of all 9 cards, pick out center ones appropriately
            start = 4 - ((estimated_count - 1) // 2)
            #print(start)
            for i in range(estimated_count):                
                card = image[upper_lefts_odd[row][start + i][0]:lower_rights_odd[row][start + i][0], upper_lefts_odd[row][start + i][1]:lower_rights_odd[row][start + i][1], :]
                plt.imshow(card)
                plt.show()
                
                name = classify_card_image(card)
                print(name)
    
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

def train_card_classifier():
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
    # take_screenshot()
    
    # uncomment to create image hash references based on image library of cards
    # width, height, names, hashes = train_card_classifier()
    # pickle.dump(width, open('./classifier/width.p', 'wb'))
    # pickle.dump(height, open('./classifier/height.p', 'wb'))
    # pickle.dump(names, open('./classifier/names.p', 'wb'))
    # pickle.dump(hashes, open('./classifier/hashes.p', 'wb'))
    
    # load classifier parameters from files
    width = pickle.load(open('./classifier/width.p', 'rb'))
    height = pickle.load(open('./classifier/height.p', 'rb'))
    ref_names = pickle.load(open('./classifier/names.p', 'rb'))
    ref_hashes = pickle.load(open('./classifier/hashes.p', 'rb'))
    
    # image = cv2.imread('./development_screenshots/sample_board_8_cards.png')
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    
    identify_board()
    
    # # 493, 353 - 10, 89 = 483, 264
    # # 410, 229 - 10, 89 = 400, 140
    # #card = image[140:264, 400:483]
    # color = hsv_image[263:264, 482:483]
    # print(color[0][0])
    # # plt.imshow(color)
    # # plt.show()
    # lower_gold = np.array([21, 50, 100])
    # upper_gold = np.array([25, 230, 255])
    
    # mask = cv2.inRange(hsv_image, lower_gold, upper_gold)
    # plt.imshow(mask)
    # plt.show()
    
    # name = classify_card_image(card)
    # print(name)
    
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