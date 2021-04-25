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

TODO: Recognize symbols in upper left of card.
"""

import cv2
from glob import glob
import imagehash
import imageio
# from keras.datasets import mnist
# from keras.models import load_model
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
# from keras.utils import to_categorical
from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
import pickle
from PIL import Image
import pyautogui
import pytesseract
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

ref_names = []
ref_hashes = []
digit_hashes = []
ref_digits = []

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
    
    fraction_x = 0.2
    fraction_y = 0.25
    image = card[int(card.shape[0] * fraction_x):-int(card.shape[0] * fraction_x), int(card.shape[1] * fraction_y):-int(card.shape[1] * fraction_y)]
    
    # resize image
    #image = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)
    
    im = Image.fromarray(image)
    active_hash = imagehash.phash(im)
    
    min_distance = 1000000000
    best_match = ''
    for i in range(len(ref_hashes)):
        current_hash = ref_hashes[i]
        distance = 0
        # for j in range(len(active_hash)):
        #     if active_hash[j] != current_hash[j]:
        #         distance += 1
        distance = abs(active_hash - current_hash)
        if distance < min_distance:
            min_distance = distance
            best_match = ref_names[i]
    
    return best_match

# def classify_digit_keras(image):
    
#     image = cv2.resize(image, (28, 28), interpolation = cv2.INTER_AREA)
    
#     model = load_model("./classifier/keras_model.h5")

#     img_rows = 28
#     img_cols = 28
#     image = image.reshape(1, img_rows, img_cols, 1)
    
#     image = image / 255

#     # predict digit
#     prediction = model.predict(image)
#     return prediction.argmax()

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
    
    #image = cv2.imread('./development_screenshots/sample_bleed.png')
    #image = cv2.imread('./development_screenshots/sample_defender.png')
    #image = cv2.imread('./development_screenshots/sample_doomed.png')
    #image = cv2.imread('./development_screenshots/sample_immunity_sleeping_order.png')
    #image = cv2.imread('./development_screenshots/sample_poison.png')
    #image = cv2.imread('./development_screenshots/sample_resilience.png')
    #image = cv2.imread('./development_screenshots/sample_rupture.png')
    #image = cv2.imread('./development_screenshots/sample_spying_locked_cooldown_veil.png')
    #image = cv2.imread('./development_screenshots/sample_vitality_shield.png')
    #image = cv2.imread('./development_screenshots/sample_board_9_cards.png')
    #image = cv2.imread('./development_screenshots/sample_board_8_cards.png')
    #image = cv2.imread('./development_screenshots/sample_armor.png')
    image = cv2.imread('./development_screenshots/sample_order_red_charge.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    diamond_heights = [134, 267, 422, 589]
    left_starts = [363, 345, 335, 294]
    #left_starts = [363, 345, 380, 294] # 3rd row annoying for current board
    card_starts = [363, 345, 315, 294]
    row_widths = [867, 909, 959, 1012]
    widths = [97, 101, 107, 114]
    
    # coordinates of cards, by row
    upper_lefts_odd = [[[121, 367], [121, 463], [121, 560], [121, 658], [121, 754], [121, 851], [121, 948], [121, 1045], [121, 1142]],
                        [[252, 347], [252, 449], [252, 550], [252, 652], [252, 753], [252, 855], [252, 957], [252, 1058], [252, 1159]],
                        [[406, 322], [406, 429], [406, 535], [406, 642], [406, 750], [406, 857], [406, 964], [406, 1070], [406, 1178]],
                        [[570, 295], [570, 409], [570, 522], [570, 634], [570, 747], [570, 860], [570, 973], [570, 1085], [570, 1199]]]
    upper_rights_odd = [[[121, 458], [121, 555], [121, 653], [121, 749], [121, 846], [121, 943], [121, 1040], [121, 1137], [121, 1233]],
                        [[252, 444], [252, 545], [252, 647], [252, 748], [252, 850], [252, 952], [252, 1053], [252, 1154], [252, 1253]],
                        [[406, 422], [406, 530], [406, 637], [406, 745], [406, 852], [406, 958], [406, 1065], [406, 1172], [406, 1279]],
                        [[570, 403], [570, 516], [570, 627], [570, 741], [570, 854], [570, 967], [570, 1079], [570, 1191], [570, 1305]]]
    lower_lefts_odd = [[[239, 349], [239, 450], [239, 551], [239, 652], [239, 753], [239, 853], [239, 955], [239, 1055], [239, 1156]],
                        [[384, 326], [384, 432], [384, 538], [384, 644], [384, 750], [384, 856], [384, 962], [384, 1068], [384, 1174]],
                        [[554, 298], [554, 411], [554, 523], [554, 635], [554, 747], [554, 859], [554, 971], [554, 1083], [554, 1195]],
                        [[733, 270], [733, 389], [733, 507], [733, 625], [733, 744], [733, 861], [733, 980], [733, 1099], [733, 1218]]]
    lower_rights_odd = [[[239, 444], [239, 546], [239, 647], [239, 748], [239, 848], [239, 950], [239, 1050], [239, 1151], [239, 1252]],
                        [[384, 425], [384, 533], [384, 639], [384, 745], [384, 851], [384, 957], [384, 1063], [384, 1169], [384, 1275]],
                        [[554, 404], [554, 517], [554, 629], [554, 741], [554, 853], [554, 966], [554, 1077], [554, 1189], [554, 1301]],
                        [[733, 382], [733, 501], [733, 620], [733, 739], [733, 856], [733, 975], [733, 1093], [733, 1211], [733, 1330]]]
    upper_lefts_even = [[[121, 414], [121, 511], [121, 608], [121, 704], [121, 803], [121, 897], [121, 994], [121, 1091]],
                        [[252, 395], [252, 497], [252, 598], [252, 701], [252, 803], [252, 902], [252, 1004], [252, 1106]],
                        [[407, 374], [407, 479], [407, 586], [407, 696], [407, 803], [407, 908], [407, 1015], [407, 1123]],
                        [[569, 348], [569, 462], [569, 576], [569, 690], [569, 803], [569, 914], [569, 1027], [569, 1139]]]
    upper_rights_even = [[[121, 505], [121, 603], [121, 700], [121, 796], [121, 893], [121, 990], [121, 1086], [121, 1182]],
                        [[252, 491], [252, 593], [252, 694], [252, 795], [252, 897], [252, 999], [252, 1101], [252, 1202]],
                        [[407, 474], [407, 582], [407, 689], [407, 797], [407, 904], [407, 1010], [407, 1116], [407, 1224]],
                        [[569, 458], [569, 570], [569, 683], [569, 796], [569, 908], [569, 1021], [569, 1134], [569, 1247]]]
    lower_lefts_even = [[[240, 398], [240, 498], [240, 599], [240, 701], [240, 803], [240, 901], [240, 1002], [240, 1103]],
                        [[384, 376], [384, 483], [384, 589], [384, 697], [384, 804], [384, 906], [384, 1012], [384, 1119]],
                        [[554, 352], [554, 465], [554, 577], [554, 690], [554, 804], [554, 912], [554, 1024], [554, 1136]],
                        [[734, 327], [734, 445], [734, 563], [734, 685], [734, 804], [734, 919], [734, 1037], [734, 1156]]]
    lower_rights_even = [[[240, 492], [240, 594], [240, 695], [240, 796], [240, 896], [240, 997], [240, 1098], [240, 1200]],
                        [[384, 477], [384, 583], [384, 690], [384, 796], [384, 901], [384, 1007], [384, 1113], [384, 1220]],
                        [[554, 460], [554, 573], [554, 684], [554, 797], [554, 908], [554, 1020], [554, 1132], [554, 1246]],
                        [[734, 441], [734, 559], [734, 678], [734, 797], [734, 915], [734, 1033], [734, 1152], [734, 1270]]]
    
    for row in range(4):
        
        hsv_image = cv2.cvtColor(image[diamond_heights[row] - 15:diamond_heights[row] + 15, left_starts[row]:left_starts[row] + row_widths[row]], cv2.COLOR_RGB2HSV)
        lower1 = np.array([12, 50, 50])
        #upper1 = np.array([30, 150, 150])
        upper1 = np.array([30, 200, 200])
        
        # lower2 = np.array([0, 50, 50])
        # upper2 = np.array([2, 150, 150])
        
        mask = cv2.inRange(hsv_image, lower1, upper1)
        # mask1 = cv2.inRange(hsv_image, lower1, upper1)
        # mask2 = cv2.inRange(hsv_image, lower2, upper2)
        # mask = np.logical_or(mask1, mask2)
        # plt.figure(figsize=(20, 20))
        # plt.imshow(mask)
        # plt.show()
        
        estimated_count = 0
        
        i = 0
        while (i < np.shape(hsv_image)[1]):
            active_sum = sum(mask[:, i])
            if (row == 2 and i < 50): # 3rd row annoying
                i += 1
            elif active_sum > 5 * 255:
                estimated_count += 1
                i += widths[row]
                #print(i)
                #estimated_count = int(round(9 - 2 * i / widths[row]))
                #print(estimated_count)
            else:
                i += 1
        #print('Estimated Card Count: ' + str(estimated_count))
        
        # Recover all cards based on estimated count, then identify them
        if estimated_count % 2 == 0 and estimated_count > 0:
            # start from coordinates of all 8 cards, pick out center ones appropriately
            start = 4 - (estimated_count // 2)
            for i in range(estimated_count):
                card = image[upper_lefts_even[row][start + i][0]:lower_rights_even[row][start + i][0], upper_lefts_even[row][start + i][1]:lower_rights_even[row][start + i][1], :]
                
                # plt.imshow(card)
                # plt.show()
                
                # Straighten and resize card before classification
                corners = [(upper_lefts_even[row][start + i][1], upper_lefts_even[row][start + i][0]),
                           (upper_rights_even[row][start + i][1], upper_rights_even[row][start + i][0]),
                           (lower_rights_even[row][start + i][1], lower_rights_even[row][start + i][0]),
                           (lower_lefts_even[row][start + i][1], lower_lefts_even[row][start + i][0])]
                width = np.shape(card)[1]
                height = np.shape(card)[0]
                target = [(0, 0), (width, 0), (width, height), (0, height)]
                H, _ = cv2.findHomography(np.array(corners), np.array(target))
                
                # Apply matrix H to source image.
                card = cv2.warpPerspective(image, H, (width, height))
                
                # print('Reshaped')
                # plt.imshow(card)
                # plt.show()
                
                identify_card(card)
                
        else: # estimated_count % 2 == 1
            # start from coordinates of all 9 cards, pick out center ones appropriately
            start = 4 - ((estimated_count - 1) // 2)
            #print(start)
            for i in range(estimated_count):                
                card = image[upper_lefts_odd[row][start + i][0]:lower_rights_odd[row][start + i][0], upper_lefts_odd[row][start + i][1]:lower_rights_odd[row][start + i][1], :]
                
                # plt.imshow(card)
                # plt.show()
                
                # Straighten and resize card before classification
                corners = [(upper_lefts_odd[row][start + i][1], upper_lefts_odd[row][start + i][0]),
                           (upper_rights_odd[row][start + i][1], upper_rights_odd[row][start + i][0]),
                           (lower_rights_odd[row][start + i][1], lower_rights_odd[row][start + i][0]),
                           (lower_lefts_odd[row][start + i][1], lower_lefts_odd[row][start + i][0])]
                width = np.shape(card)[1]
                height = np.shape(card)[0]
                target = [(0, 0), (width, 0), (width, height), (0, height)]
                H, _ = cv2.findHomography(np.array(corners), np.array(target))
                
                # Apply matrix H to source image.
                card = cv2.warpPerspective(image, H, (width, height))
                
                # print('Reshaped')
                # plt.imshow(card)
                # plt.show()
                
                identify_card(card)

def identify_card(card):
    
    card = cv2.resize(card, (249, 357), interpolation = cv2.INTER_AREA)
    
    plt.imshow(card)
    plt.show()
    #print(np.shape(card))
    
    name = classify_card_image(card)
    print('Name: ' + name)
    
    # TODO: Identify card faction?  May not need this if card name is super reliable.
    # Improve classifications by using faction information from csv
    # factions = ['Monsters', 'Nilfgaard', 'Northern Realms', 'Scoia\'tael', 'Skellige', 'Syndicate']
    # rgb_colors = np.array([[[75, 22, 20], [22, 27, 29], [23, 51, 89], [51, 58, 17], [59, 47, 77], [83, 32, 0]]], np.float32)
    # #print(rgb_colors)
    # hsv_colors = cv2.cvtColor(rgb_colors, cv2.COLOR_RGB2HSV)
    
    # # TODO: Identify faction from background color in diamond
    # x_percent = 10
    # y_percent = 5
    
    # x = int(round(np.shape(card)[0] * x_percent / 100))
    # y = int(round(np.shape(card)[0] * y_percent / 100))
    
    # rgb_faction = card[x:x+1, y:y+1, :]
    # hsv_faction = cv2.cvtColor(rgb_faction, cv2.COLOR_RGB2HSV)
    # #print(hsv_faction)
    
    # best_faction = ''
    # min_distance = 10000
    # for i in range(len(factions)):
    #     distance = np.linalg.norm(rgb_faction[0] - rgb_colors[0][i])
    #     # distance = abs(hsv_faction[0][0][0] - hsv_colors[0][i][0])
    #     if distance < min_distance:
    #         best_faction = factions[i]
    #         min_distance = distance
    # print(best_faction)
    
    # TODO: Recognize the back of cards as well for traps
    # TODO: Copy cardbacks from site
    
    # Identify card power
    
    # Isolate pixels that stand out in diamond      
    # Mask white, red, or green number in upper left
    # White: (187, 178, 156)
    # Green: (118, 255, 121)
    # Red: (255, 60, 60)
    # Isolate digits, then classify each digit with imagehash
      
    # isolate upper left of card
    h_fraction_left = 0.05
    h_fraction_right = 0.28
    v_fraction_upper = 0.05
    v_fraction_lower = 0.16
    #v_fraction = # 0.31
    
    width_left = int(round(h_fraction_left * np.shape(card)[1]))
    width_right = int(round(h_fraction_right * np.shape(card)[1]))
    #height = int(round(v_fraction * np.shape(card)[1]))
    height_upper = int(round(v_fraction_upper * np.shape(card)[0]))
    height_lower = int(round(v_fraction_lower * np.shape(card)[0]))
    
    upper_left_card = card[height_upper:height_lower, width_left:width_right, :]
    
    # filter out orange from shield
    upper_left_hsv = cv2.cvtColor(upper_left_card, cv2.COLOR_RGB2HSV)
    
    lower_green = np.array([55, 50, 100])
    upper_green = np.array([65, 255, 255])
    lower_red = np.array([0, 190, 150])
    upper_red = np.array([20, 220, 256])
    lower_white = np.array([20, 20, 0])
    upper_white = np.array([25, 60, 255])
    
    mask1 = cv2.inRange(upper_left_hsv, lower_green, upper_green)
    mask2 = cv2.inRange(upper_left_hsv, lower_red, upper_red)
    mask3 = cv2.inRange(upper_left_hsv, lower_white, upper_white)
    
    # plt.imshow(mask1)
    # plt.show()
    
    mask = mask1 | mask2 | mask3
    
    # plt.imshow(mask)
    # plt.show()
    
    upper_left_card = mask
    
    # plt.imshow(upper_left_card)
    # plt.show()
    
    #upper_left_card = cv2.cvtColor(upper_left_card, cv2.COLOR_RGB2GRAY)
    
    #_, upper_left_card = cv2.threshold(upper_left_card, 10, 255, cv2.THRESH_BINARY)
    
    #upper_left_card = cv2.GaussianBlur(upper_left_card,(5,5),0)
    
    # ret3, upper_left_card = cv2.threshold(upper_left_card,127,255,cv2.THRESH_BINARY)#+cv2.THRESH_OTSU
    #upper_left_card = 255 - upper_left_card
    
    # plt.imshow(upper_left_card)
    # plt.show()
    
    #upper_left_card = cv2.resize(upper_left_card, (int(round(ref_digits[0].shape[1])), int(round(ref_digits[0].shape[0]))), interpolation = cv2.INTER_AREA)
    #ret, upper_left_card = cv2.threshold(upper_left_card, 127, 255, cv2.THRESH_BINARY)
    power = identify_number(upper_left_card)
    print('Power: ' + str(power))
    
    # Identify card armor
    # Isolate upper right of card image
    # TODO: Count number of yellow-ish pixels?
    armor_present = False
    
    h_fraction_left = 0.25
    h_fraction_right = 0.05
    v_fraction_lower = 0.17
    v_fraction_upper = 0.05
    
    armor_image = card[int(round(v_fraction_upper * card.shape[0])):int(round(v_fraction_lower * card.shape[0])), -int(round(h_fraction_left * card.shape[1])):-int(round(h_fraction_right * card.shape[1]))]
    # plt.imshow(armor_image)
    # plt.show()
    
    armor_hsv = cv2.cvtColor(armor_image, cv2.COLOR_RGB2HSV)
    lower_bound = np.array([20, 30, 100])
    upper_bound = np.array([30, 50, 256])
    
    # plt.hist(armor_hsv[:,:,0])
    # plt.show()
    
    mask = cv2.inRange(armor_hsv, lower_bound, upper_bound)
    
    # plt.imshow(mask)
    # plt.show()
    
    armor_image = cv2.cvtColor(armor_image, cv2.COLOR_RGB2GRAY)
    if np.sum(mask) > 200 * 255:
        armor_present = True
    #print(armor_present)
    if armor_present:
        #np.set_printoptions(threshold=np.inf)
        #print(armor_image)
        armor = identify_number(mask)
        print('Armor: ' + str(armor))
    
    # Identify vitality or bleed (with amount) or neither
    vitality_bleed_image = card[66:100, 10:60, :]
    
    lower_bound_green = np.array([35, 100, 100])
    upper_bound_green = np.array([45, 256, 256])
    
    # check for green or red color
    vitality_bleed_hsv = cv2.cvtColor(vitality_bleed_image, cv2.COLOR_RGB2HSV)
    
    mask = cv2.inRange(vitality_bleed_hsv, lower_bound_green, upper_bound_green)
    # plt.imshow(mask)
    # plt.show()
    if np.sum(mask) > 200 * 255:
        # Find vitality number
        vitality_image = card[105:148, 20:55, :]
        vitality_image_hsv = cv2.cvtColor(vitality_image, cv2.COLOR_RGB2HSV)
        
        lower_white = np.array([10, 20, 0])
        upper_white = np.array([30, 60, 255])
        
        mask = cv2.inRange(vitality_image_hsv, lower_white, upper_white)
        
        vitality_amount = identify_number(mask)
        print('Vitality: ' + str(vitality_amount))
        
        # plt.imshow(mask)
        # plt.show()
    
    lower_bound_red = np.array([-4, 100, 100])
    upper_bound_red = np.array([4, 256, 256])
    
    mask = cv2.inRange(vitality_bleed_hsv, lower_bound_red, upper_bound_red)
    # plt.imshow(mask)
    # plt.show()
    if np.sum(mask) > 200 * 255:
        # Find vitality number
        vitality_image = card[105:148, 20:55, :]
        vitality_image_hsv = cv2.cvtColor(vitality_image, cv2.COLOR_RGB2HSV)
        
        lower_white = np.array([10, 20, 0])
        upper_white = np.array([30, 60, 255])
        
        mask = cv2.inRange(vitality_image_hsv, lower_white, upper_white)
        
        bleed_amount = identify_number(mask)
        print('Bleed: ' + str(bleed_amount))
        
    # plt.imshow(vitality_bleed_image)
    # plt.show()
    
    # Card statuses identified
    # defender
    # doomed
    # immunity
    # locked
    # poisoned
    # resilience
    # rupture
    # shield
    # spying
    # veil
    # all but locked show up on left hand side
    # don't plan for more than 3 at once
    
    # TODO: Include Bounty!
    
    # Extract status images once each
    # veil = card[312:350, 16:60, :]
    # plt.imshow(veil)
    # plt.show()
    # if name == 'temerian drummer':
    #     shield_bgr = cv2.cvtColor(shield, cv2.COLOR_RGB2BGR)
    #     cv2.imwrite('./statuses/Shield.png', shield_bgr)
    
    # Search for status images on left column
    files = glob('./statuses/*.png')
    for file in files:
        image = cv2.imread(file)
        file = file.replace('\\', '/')
        status_name = file.split('/')[-1][:-4]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # plt.imshow(card[:, 10:70, :])
        # plt.show()
        
        res = cv2.matchTemplate(card[:, 10:70, :],image,cv2.TM_CCOEFF_NORMED)
        threshold = 0.80
        
        if (len(np.where(res > threshold)[0]) > 0):
            print(status_name)
    
    # TODO: Identify presence of card order/charge/cooldown ability
    # TODO: Identify order ability status (gray, red, green, locked, or cooldown) if present
    # TODO: Identify number of order charges or cooldown amount if present
    
    # TODO: Identify if a card is boosted, damaged, or neither from power color
    
    # TODO: Collect example image with special card, and artifact
    # TODO: Recognize stratagem, artifact, and special card symbols and don't identify power in those cases
    
    # TODO: Improve identification of 2-digit power/armor
    # This relies on optimizing the cutoff of the corners
    # Also have an issue identifying gap between digits
    
    # TODO: Single digit identification is not perfect
    # Try registering boundary of diamond?
    
    # TODO: Put all collected information into the Card datatype

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

def identify_allied_hand():
    image = cv2.imread('./development_screenshots/sample_hand_10_cards.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # TODO: Identify number of cards in allied hand using number in bottom right
    # 854, 1502, 30, 76
    # Try to identify "/ 10" then look to the left of it
    # Red text means 10 cards
    plt.imshow(image)
    plt.show()
    
    # TODO: Extract card images from allied hand
    # Use upper left corner, upper right corner to extract upper-left quarter of card
    # 0 cards to 10 cards
    upper_left_corners = [[], [[736, 724]], [[738, 670], [736, 780]], 
                          [[742, 616], [735, 725], [736, 834]],
                          [[746, 561], [737, 670], [735, 780], [737, 890]],
                          [[752, 508], [741, 616], [736, 725], [735, 834], [740, 945]],
                          [[762, 455], [747, 562], [737, 671], [734, 780], [736, 890], [745, 1000]],
                          [[771, 402], [753, 509], [740, 616], [735, 726], [734, 835], [739, 945], [751, 1054]],
                          [[782, 350], [761, 456], [746, 562], [736, 671], [733, 780], [735, 889], [743, 999], [758, 1109]],
                          []]
    upper_right_corners = [[], [[736, 876]], [[734, 817], [739, 930]],
                           [[734, 763], [736, 873], [743, 986]],
                           [[736, 709], [734, 819], [739, 929], [749, 1041]],
                           [[738, 654], [733, 764], [735, 874], [742, 984], [756, 1096]],
                           [[741, 601], [734, 709], [732, 818], [737, 929], [748, 1037], [765, 1150]],
                           [[746, 547], [737, 656], [732, 764], [734, 876], [741, 983], [754, 1092], [775, 1204]],
                           [[753, 494], [741, 601], [733, 709], [732, 819], [736, 928], [747, 1038], [764, 1147], [787, 1258]],
                           []]
    lower_left_edge = [[], [[896, 724]], [[896, 675], [897, 776]],
                          [[897, 624], [897, 726], [897, 827]],
                          [[897, 572], [898, 675], [897, 776], [897, 878]],
                          [[897, 524], [898, 625], [897, 726], [897, 827], [897, 929]],
                          [[898, 477], [898, 575], [898, 675], [898, 776], [898, 877], [898, 980]],
                          [[897, 423], [897, 524], [898, 626], [897, 726], [897, 827], [898, 928], [897, 1032]],
                          [[898, 371], [898, 475], [898, 575], [898, 676], [897, 776], [898, 877], [898, 979], [898, 1083]],
                          []]
    
    # TODO: Convert card images to name, power
    
    

def identify_number(image):
    
    # plt.imshow(image, 'gray')
    # plt.show()
    
    # remove corners
    jump_in = 22
    for i in range(jump_in):
        for j in range(jump_in):
            if i < jump_in - j:
                image[i, j] = 0
                image[image.shape[0] - i - 1, j] = 0
                image[i, image.shape[1] - j - 1] = 0
                image[image.shape[0] - i - 1, image.shape[1] - j - 1] = 0
    
    min_count_kept = 5
    
    # restrict to rows/columns with nonzero entries
    top = 0
    while (top < np.shape(image)[0] and np.sum(image[top, :]) < min_count_kept * 255):
        top += 1
        
    bottom = image.shape[0] - 1
    while (bottom >= 0 and np.sum(image[bottom, :]) < min_count_kept * 255):
        bottom -= 1
    bottom += 1
    
    left = 0
    while (left < np.shape(image)[1] and np.sum(image[:, left]) < min_count_kept * 255):
        left += 1
        
    right = image.shape[1] - 1
    while (right >= 0 and np.sum(image[:, right]) < min_count_kept * 255):
        right -= 1
    right += 1
    
    image = image[top:bottom, left:right]
    
    # plt.imshow(image, 'gray')
    # plt.show()
    
    # Identify number of digits by scanning vertically left-to-right
    digit_count = 0
    hit = False
    previous_hit = False
    digit_starts = []
    digit_ends = []
    for i in range(np.shape(image)[1]):
        active_sum = np.sum(image[:, i])
        hit = (active_sum >= 3 * 255)
        if hit and not previous_hit:
            digit_count += 1
            digit_starts.append(i)
        if not hit and previous_hit:
            digit_ends.append(i)
        previous_hit = hit
        #print(i, hit)
    digit_ends.append(image.shape[1])
    
    # print(str(digit_count) + ' digit(s)')
    # print(digit_starts, digit_ends)
    
    digit_string = ''
    
    for i in range(len(digit_starts)):
    
        image_2 = image[:, digit_starts[i]:digit_ends[i]]
        
        image_2 = cv2.resize(image_2, (50, 50), interpolation = cv2.INTER_AREA)
        
        min_mse = 100000000000
        for i in range(len(ref_digits)):
            digit = ref_digits[i]
            mse = np.sum((image_2.astype("float") - digit.astype("float")) ** 2)
            if mse < min_mse:
                min_mse = mse
                best_digit = i
        digit_string += str(best_digit)
    
    if represents_int(digit_string):
        power = int(digit_string)
    else:
        power = 0
    
    return power

def identify_number_of_enemy_cards():
    # identify the number of cards in the enemy's hand
    pass

def identify_opponent_card():
    # check if enemy is playing a card
    # if they are, recognize it from the image
    # return card name
    # if not, return ''
    pass

def identify_mulligan_choices():
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
        
        name = identify_card(card)
        names.append(name)
        
        # fraction_x = 0.2
        # fraction_y = 0.25
        # image = card[int(card.shape[0] * fraction_x):-int(card.shape[0] * fraction_x), int(card.shape[1] * fraction_y):-int(card.shape[1] * fraction_y)]
        
        # # resize image
        # #image = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)
        
        # im = Image.fromarray(image)
        # active_hash = imagehash.phash(im)
        
        # min_distance = 1000000000
        # best_match = ''
        # for i in range(len(hashes)):
        #     current_hash = hashes[i]
        #     distance = abs(active_hash - current_hash)
        #     if distance < min_distance:
        #         min_distance = distance
        #         best_match = names[i]
        # names.append(best_match)
    
    return names, centers

def identify_number_of_mulligans():
    # on the mulligan screen, identify number of mulligans to be made
    # TODO: Use custom imagehash classifier for a screenshot of digits 1 - 5
    pass

def identify_scores():
    # identify total scores on the righthand side of the board
    pass

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

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def take_screenshot():
    # Screenshot the whole game window and save it out
    myScreenshot = pyautogui.screenshot(region=(0, 31, 1600, 900))
    myScreenshot.save('./screenshots/active_screen.png')

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
        
        image = cv2.resize(image, (100, 150), interpolation = cv2.INTER_AREA)
        
        fraction_x = 0.2
        fraction_y = 0.25
        image = image[int(image.shape[0] * fraction_x):-int(image.shape[0] * fraction_x), int(image.shape[1] * fraction_y):-int(image.shape[1] * fraction_y)]
        
        # scale_percent = 100 # percent of original size
        # if scale_percent != 100:
        #     width = int(image.shape[1] * scale_percent / 100)
        #     height = int(image.shape[0] * scale_percent / 100)
        #     dim = (width, height)
              
        #     # resize image
        #     image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        
        # if 'an craite longship' in name:
        #     plt.imshow(image)
        #     plt.show()
        
        # print()
        # print()
        
        im = Image.fromarray(image)
        active_hash = imagehash.phash(im)
        hashes.append(active_hash)
        
    return names, hashes

def train_digit_classifier():
    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    hashes = []
    for digit in digits:
        if digit == 0:
            digit = 10
        file = './power_recognition/' + str(digit) + '.png'
        
        # Load image, focus on diamond, extract white part, hash it, save it
        image = cv2.imread(file)
        card = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # isolate upper left of card (slightly to the lower right of in-game cards)
        h_fraction_left = 0.07
        h_fraction_right = 0.27
        v_fraction_upper = 0.05
        v_fraction_lower = 0.19
        #v_fraction = # 0.31
        if digit == 10:
            h_fraction_left = 0.15
            h_fraction_right = 0.28
        
        width_left = int(round(h_fraction_left * np.shape(card)[1]))
        width_right = int(round(h_fraction_right * np.shape(card)[1]))
        #height = int(round(v_fraction * np.shape(card)[1]))
        height_upper = int(round(v_fraction_upper * np.shape(card)[0]))
        height_lower = int(round(v_fraction_lower * np.shape(card)[0]))
        
        upper_left_card = card[height_upper:height_lower, width_left:width_right, :]
        upper_left_card = cv2.cvtColor(upper_left_card, cv2.COLOR_RGB2GRAY)
        
        # plt.imshow(upper_left_card)
        # plt.show()
        
        #upper_left_card = cv2.resize(upper_left_card, (int(round(ref_digits[0].shape[1])), int(round(ref_digits[0].shape[0]))), interpolation = cv2.INTER_AREA)
        #ret, upper_left_card = cv2.threshold(upper_left_card, 127, 255, cv2.THRESH_BINARY)
        blur = cv2.GaussianBlur(upper_left_card,(5,5),0)
        ret3, upper_left_card = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)#+cv2.THRESH_OTSU
        upper_left_card = upper_left_card
        
        # remove corners
        for i in range(18):
            for j in range(18):
                if i < 18 - j:
                    if digit != 10:
                        upper_left_card[i, j] = 0
                    if digit != 10:
                        upper_left_card[upper_left_card.shape[0] - i - 1, j] = 0
                    upper_left_card[i, upper_left_card.shape[1] - j - 1] = 0
                    upper_left_card[upper_left_card.shape[0] - i - 1, upper_left_card.shape[1] - j - 1] = 0  
        
        # restrict to rows/columns with nonzero entries
        top = 0
        while (np.sum(upper_left_card[top, :]) < 2 * 255):
            top += 1
            
        bottom = upper_left_card.shape[0] - 1
        while (np.sum(upper_left_card[bottom, :]) < 2 * 255):
            bottom -= 1
        bottom += 1
        
        left = 0
        while (np.sum(upper_left_card[:, left]) < 2 * 255):
            left += 1
            
        right = upper_left_card.shape[1] - 1
        while (np.sum(upper_left_card[:, right]) < 2 * 255):
            right -= 1
        right += 1
        
        upper_left_card = upper_left_card[top:bottom, left:right]
        
        upper_left_card = cv2.resize(upper_left_card, (50, 50), interpolation = cv2.INTER_AREA)
        
        # plt.imshow(upper_left_card, cmap='gray')
        # plt.show()
        
        ref_digits.append(upper_left_card)
        
        # # isolate upper left of card
        # h_fraction_left = 0.08
        # h_fraction_right = 0.15
        # v_fraction_upper = 0.09
        # v_fraction_lower = 0.27
        
        # # h_fraction_left = 0.05
        # # h_fraction_right = 0.17
        # # v_fraction_upper = 0.04
        # # v_fraction_lower = 0.26
        
        # if digit == 10:
        #     h_fraction_left = 0.10
        #     h_fraction_right = 0.17
        
        # width_left = int(round(h_fraction_left * np.shape(card)[0]))
        # width_right = int(round(h_fraction_right * np.shape(card)[0]))
        # height_upper = int(round(v_fraction_upper * np.shape(card)[1]))
        # height_lower = int(round(v_fraction_lower * np.shape(card)[1]))
        
        # upper_left_card = card[height_upper:height_lower, width_left:width_right, :]
        
        # # plt.imshow(upper_left_card)
        # # plt.show()
        
        # lower_white = (170, 160, 140)
        # upper_white = (255, 255, 255)
        
        # # lower_green = (50, 200, 50)
        # # upper_green = (200, 256, 200)
        
        # # lower_red = (250, 50, 50)
        # # upper_red = (256, 70, 70)
        
        # mask = cv2.inRange(upper_left_card, lower_white, upper_white)
        
        # #mask = cv2.resize(mask, (28, 28), interpolation = cv2.INTER_AREA)
        
        # mask = 255 - mask
        
        # mask = np.stack((mask,)*3, axis=-1)
        
        # # plt.imshow(mask)
        # # plt.show()
        
        # ref_digits.append(mask)
        
        # im = Image.fromarray(upper_left_card)
        # active_hash = imagehash.phash(im)
        # digit_hashes.append(active_hash)

# def train_keras_digit_classifier():
#     (x_train, y_train), (x_test, y_test) = mnist.load_data()
#     # index = 35
#     # print(y_train[index])
#     # plt.imshow(x_train[index], cmap='Greys')
#     # plt.show()
#     # print(x_train.shape, x_test.shape)
    
#     # save input image dimensions
#     img_rows, img_cols = 28, 28
    
#     x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
#     x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    
#     x_train = x_train / 255
#     x_test = x_test / 255
    
#     num_classes = 10

#     y_train = to_categorical(y_train, num_classes)
#     y_test = to_categorical(y_test, num_classes)
    
#     model = Sequential()
#     model.add(Conv2D(32, kernel_size=(3, 3),
#      activation='relu',
#      input_shape=(img_rows, img_cols, 1)))
#     model.add(Conv2D(64, (3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Dropout(0.25))
#     model.add(Flatten())
#     model.add(Dense(128, activation='relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(num_classes, activation='softmax'))
    
#     # model.compile(loss='sparse_categorical_crossentropy',
#     #   optimizer='adam',
#     #   metrics=['accuracy'])
#     model.compile(loss='categorical_crossentropy',
#       optimizer='adam',
#       metrics=['accuracy'])
    
#     batch_size = 128
#     epochs = 10
    
#     model.fit(x_train, y_train,
#               batch_size=batch_size,
#               epochs=epochs,
#               verbose=1,
#               validation_data=(x_test, y_test))
#     score = model.evaluate(x_test, y_test, verbose=0)
#     print('Test loss:', score[0])
#     print('Test accuracy:', score[1])
#     model.save("./classifier/keras_model.h5")
        
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
    
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Users\bwoodhouse\AppData\Local\Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Brent\AppData\Local\Tesseract-OCR\tesseract'
    
    # image = cv2.imread('./development_screenshots/tesseract_test.png')
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # text = pytesseract.image_to_string(image) #, config='digits -psm 7')
    # print('OCR: ' + text.rstrip())
    
    # pause to allow user to make Gwent window active
    time.sleep(3)
    
    # uncomment to take screenshot for development
    take_screenshot()
    
    # uncomment to create image hash references based on image library of cards
    # names, hashes = train_card_classifier()
    # pickle.dump(names, open('./classifier/names.p', 'wb'))
    # pickle.dump(hashes, open('./classifier/hashes.p', 'wb'))
    
    # load classifier parameters from files
    ref_names = pickle.load(open('./classifier/names.p', 'rb'))
    ref_hashes = pickle.load(open('./classifier/hashes.p', 'rb'))
    
    #train_keras_digit_classifier()
    
    #digit_hashes = train_digit_classifier()
    
    #train_digit_classifier()
    #identify_mulligan_choices()
    
    identify_allied_hand()
    #identify_board()
    
    #action_hard_pass()
    
    # analyze_game_state()
    # make_move()
    
    # infinite loop to keep playing more games
    # while True:
    #     analyze_game_state()
    #     make_move()
    #     time.sleep(1)