# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:39:03 2021

@author: bwoodhouse

Maintain game state while playing Gwent and take automatic actions.

Initial goals:
Automatically play a game.
Random mulligan, random plays (of trivial deck to play).
Pass if opponent passes and you are ahead in score, otherwise play to random location.
"""

import time

def analyze_game_state():
    # observe and record everything possible about the current game state
    pass

def end_game():
    # click in a few places to move back to primary menu
    pass

def initialize_game():
    # click to launch a game
    # wait until mulligan screen
    pass

def make_move():
    # follow a specified behavior pattern and click appropriately to play a card
    pass

if __name__ == "__main__":
    # recognize menu screen where a game can be launched
    # play unranked for now
    # infinite loop to keep playing more games
    while True:
        initialize_game()
        game_active = True
        my_turn = True
        while game_active:
            analyze_game_state()
            if my_turn:
                make_move()
                time.sleep(2)
        end_game()