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
    image = cv2.imread('./development_screenshots/sample_board_8_cards.png')
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
    lower_lefts_odd = [[[239, 349], [239, 450], [239, 551], [239, 652], [239, 753], [239, 853], [239, 955], [239, 1055], [239, 1156]],
                        [[384, 326], [384, 432], [384, 538], [384, 644], [384, 750], [384, 856], [384, 962], [384, 1068], [384, 1174]],
                        [[554, 298], [554, 411], [554, 523], [554, 635], [554, 747], [554, 859], [554, 971], [554, 1083], [554, 1195]],
                        [[733, 270], [733, 389], [733, 507], [733, 625], [733, 744], [733, 861], [733, 980], [733, 1099], [733, 1218]]]
    lower_rights_odd = [[[239, 444], [239, 546], [239, 647], [239, 748], [239, 848], [239, 950], [239, 1050], [239, 1151], [239, 1252]],
                        [[384, 425], [384, 533], [384, 639], [384, 745], [384, 851], [384, 957], [384, 1063], [384, 1169], [384, 1275]],
                        [[554, 404], [554, 517], [554, 629], [554, 741], [554, 853], [554, 966], [554, 1077], [554, 1189], [554, 1301]],
                        [[733, 382], [733, 501], [733, 620], [733, 739], [733, 856], [733, 975], [733, 1093], [733, 1211], [733, 1330]]]
    upper_lefts_even = [[[121, 414], [121, 511], [121, 608], [121, 702], [121, 801], [121, 897], [121, 994], [121, 1091]],
                        [[252, 395], [252, 497], [252, 598], [252, 699], [252, 801], [252, 902], [252, 1004], [252, 1106]],
                        [[407, 374], [407, 479], [407, 586], [407, 694], [407, 801], [407, 908], [407, 1015], [407, 1123]],
                        [[569, 348], [569, 462], [569, 576], [569, 688], [569, 801], [569, 914], [569, 1027], [569, 1139]]]
    upper_rights_even = [[[121, 505], [121, 603], [121, 700], [121, 796], [121, 893], [121, 990], [121, 1086], [121, 1182]],
                        [[252, 491], [252, 593], [252, 694], [252, 795], [252, 897], [252, 999], [252, 1101], [252, 1202]],
                        [[407, 474], [407, 582], [407, 689], [407, 797], [407, 904], [407, 1010], [407, 1116], [407, 1224]],
                        [[569, 458], [569, 570], [569, 683], [569, 796], [569, 908], [569, 1021], [569, 1134], [569, 1247]]]
    lower_lefts_even = [[[240, 398], [240, 498], [240, 599], [240, 699], [240, 800], [240, 901], [240, 1002], [240, 1103]],
                        [[384, 376], [384, 483], [384, 589], [384, 695], [384, 801], [384, 906], [384, 1012], [384, 1119]],
                        [[554, 352], [554, 465], [554, 577], [554, 688], [554, 801], [554, 912], [554, 1024], [554, 1136]],
                        [[734, 327], [734, 445], [734, 563], [734, 683], [734, 801], [734, 919], [734, 1037], [734, 1156]]]
    lower_rights_even = [[[240, 492], [240, 594], [240, 695], [240, 796], [240, 896], [240, 997], [240, 1098], [240, 1200]],
                        [[384, 477], [384, 583], [384, 690], [384, 796], [384, 901], [384, 1007], [384, 1113], [384, 1220]],
                        [[554, 460], [554, 573], [554, 684], [554, 797], [554, 908], [554, 1020], [554, 1132], [554, 1246]],
                        [[734, 441], [734, 559], [734, 678], [734, 797], [734, 915], [734, 1033], [734, 1152], [734, 1270]]]
    
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
                target = [(0, 0), (100, 0), (100, 150), (0, 150)]
                H, _ = cv2.findHomography(np.array(corners), np.array(target))
                
                # Apply matrix H to source image.
                card = cv2.warpPerspective(image, H, (100, 150))
                
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
                target = [(0, 0), (100, 0), (100, 150), (0, 150)]
                H, _ = cv2.findHomography(np.array(corners), np.array(target))
                
                # Apply matrix H to source image.
                card = cv2.warpPerspective(image, H, (100, 150))
                
                # print('Reshaped')
                # plt.imshow(card)
                # plt.show()
                
                identify_card(card)

def identify_card(card):
    
    plt.imshow(card)
    plt.show()
    
    name = classify_card_image(card)
    print(name)
    
    # TODO: Recognize the back of cards as well for traps
    # Copy cardbacks from site
    
    # TODO: Identify card power
    # Isolate pixels that stand out in diamond
    # Tried and failed with pytesseract
    # Next attempt: Classify digits with imagehash?
    # Need reference images from game for all powers <= 20 on every color background.
      
    # Mask white, red, or green number in upper left
    # White: (187, 178, 156)
    # Green: (118, 255, 121)
    # Red: (255, 60, 60)
    # Isolate digits, then classify each digit with imagehash
      
    # isolate upper left of card
    h_fraction = 0.21
    v_fraction_upper = 0.06
    v_fraction_lower = 0.27
    #v_fraction = # 0.31
    
    width = int(round(h_fraction * np.shape(card)[0]))
    #height = int(round(v_fraction * np.shape(card)[1]))
    height_upper = int(round(v_fraction_upper * np.shape(card)[1]))
    height_lower = int(round(v_fraction_lower * np.shape(card)[1]))
    
    upper_left_card = card[height_upper:height_lower, 0:width, :]
    
    plt.imshow(upper_left_card)
    plt.show()
    
    lower_white = (170, 160, 140)
    upper_white = (210, 200, 170)
    
    lower_green = (50, 200, 50)
    upper_green = (200, 256, 200)
    
    lower_red = (250, 50, 50)
    upper_red = (256, 70, 70)
    
    mask_1 = cv2.inRange(upper_left_card, lower_white, upper_white)
    mask_2 = cv2.inRange(upper_left_card, lower_green, upper_green)
    mask_3 = cv2.inRange(upper_left_card, lower_red, upper_red)
    
    mask = np.logical_or(mask_1, mask_2, mask_3)
    
    # plt.imshow(1 - mask, cmap='gray')
    # plt.show()
    
    # Create custom kernel
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    # # Perform closing (dilation followed by erosion)
    # mask = 255 - 255 * cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # #mask = cv2.blur(mask, (2, 2))
    
    # mask = np.stack((mask,)*3, axis=-1)
    
    # #print(mask)
    
    # cv2.dilate(mask, (5, 5), mask)
    
    # # mask = cv2.resize(mask, (20, 10), interpolation = cv2.INTER_AREA)
    
    # plt.imshow(mask)
    # plt.show()
    
    # text = pytesseract.image_to_string(mask, config='digits -psm 7')
    # print('OCR: ' + text.rstrip())
    
    # TODO: Identify card armor
    # TODO: Identify card statuses
    # TODO: Identify presence of card order ability
    # TODO: Identify order ability status (gray, red, or green) if present
    # TODO: Identify number of order charges if present

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
        
        fraction_x = 0.2
        fraction_y = 0.25
        image = card[int(card.shape[0] * fraction_x):-int(card.shape[0] * fraction_x), int(card.shape[1] * fraction_y):-int(card.shape[1] * fraction_y)]
        
        # resize image
        #image = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)
        
        im = Image.fromarray(image)
        active_hash = imagehash.phash(im)
        
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
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\bwoodhouse\AppData\Local\Tesseract-OCR\tesseract.exe'
    
    # image = cv2.imread('./development_screenshots/tesseract_test.png')
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # text = pytesseract.image_to_string(image) #, config='digits -psm 7')
    # print('OCR: ' + text.rstrip())
    
    # pause to allow user to make Gwent window active
    time.sleep(3)
    
    # uncomment to take screenshot for development
    # take_screenshot()
    
    # uncomment to create image hash references based on image library of cards
    # names, hashes = train_card_classifier()
    # pickle.dump(names, open('./classifier/names.p', 'wb'))
    # pickle.dump(hashes, open('./classifier/hashes.p', 'wb'))
    
    # load classifier parameters from files
    ref_names = pickle.load(open('./classifier/names.p', 'rb'))
    ref_hashes = pickle.load(open('./classifier/hashes.p', 'rb'))
    
    identify_board()
    
    #action_hard_pass()
    
    # analyze_game_state()
    # make_move()
    
    # infinite loop to keep playing more games
    # while True:
    #     analyze_game_state()
    #     make_move()
    #     time.sleep(1)