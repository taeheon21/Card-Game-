from collections import deque
import random


class GameAI:
    def __init__(self):
              self.player_move_history = deque(maxlen=10)
              self.special_cards = ['2S', '9S']
              self.player_used_special = False
              self.player_last_special = None
