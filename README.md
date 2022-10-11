# AutoGwent
This is an unfinished personal project meant to explore computer vision and machine learning problems related to an online collectible card game called Gwent.
Primary accomplishments so far:
1. Almost complete game emulator in Python (as of 2021 Gwent rules and cards)
2. Take periodic screenshots of a live game with an AI player, then determines the current game status (whose turn, cards in hand, cards on the board, card statuses, etc.)
   - Note highly accurate card classification based on hashing an image; also usually works on video cards
   - Digit recognition to determine card power, armor, etc.
3. Run a Monte Carlo Tree Search to identify best courses of action, looking forward as far as possible in the time alloted for a turn.

Planned:
Better play heuristics to explore the game tree.
Reinforcement learning of appropriate strategies.
