# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:39:03 2021

@author: bwoodhouse

Maintain game state while playing Gwent and take automatic actions.

Initial goals:
Automatically play a game.
Random mulligan, random plays (of trivial deck to play).
Pass if opponent passes and you are ahead in score, otherwise play to random location.

TODO: Take a few screenshots of each type of screen for development purposes.
"""

import imageio
from matplotlib import pyplot as plt
import numpy as np
import pyautogui
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

def make_mulligans():
    # identify and click cards for mulligan
    
    # TODO: Load test image to isolate cards
    
    # TODO: Identify cards by comparing to saved images
    
    # TODO: Make sure execution is < 3 seconds total
    
    # TODO: Randomly select card to mulligan at this point
    
    pass

def take_screenshot():
    # Screenshot the whole game window and save it out
    myScreenshot = pyautogui.screenshot(region=(0, 31, 1600, 900))
    myScreenshot.save('./screenshots/active_screen.png')

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
    
    make_mulligans()
    
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