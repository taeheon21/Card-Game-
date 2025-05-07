import pickle
import random
import numpy as np
from game import Game



# Simple decision tree nodes
class Node:
    pass

class DecisionNode:
    def __init__(self, cond=None, action=None):
        # cond: to judge, action: to act
        self.cond = cond
        self.action = action
        self.left = None  # when conditon is True
        self.right = None  # when condition is False

# Condition

def is_figure_high(game):
    return game.current_figure.value >= 8


def has_high_cards(game):
    for c in game.computer.hand:
        if 7 <= c.value <= 10:
            return True
    return False



def has_low_cards(game):
    for c in game.computer.hand:
        if 2 <= c.value <= 4:
            return True
    return False


def has_special_card(game):
    for c in game.computer.hand:
        if c.code in ['2S', '9S']:
            return True
    return False


# Action

def play_high_val(game):
    play_choice('high', game.computer)



def play_low_val(game):
    play_choice('low', game.computer)


def play_special(game):
    play_choice('special', game.computer)



def play_highest(game):
    play_choice('highest', game.computer)




def play_lowest(game):
    play_choice('lowest', game.computer)


def play_choice(choice, player):
    if choice == 'high':
        player.play_high_value_card()
    elif choice == 'low':
        player.play_low_value_card()
    elif choice == 'special':
        player.play_special_card()
    elif choice == 'highest':
        player.play_highest_value_card()
    else:
        player.play_lowest_value_card()



# Build the decision tree
root = DecisionNode(cond=is_figure_high)
# figure>=8
root.left = DecisionNode(cond=has_high_cards)
root.left.left  = DecisionNode(action=play_high_val)
root.left.right = DecisionNode(cond=has_special_card)
root.left.right.left  = DecisionNode(action=play_special)
root.left.right.right = DecisionNode(action=play_highest)
# figure<8
root.right = DecisionNode(cond=has_low_cards)
root.right.left  = DecisionNode(action=play_low_val)
root.right.right = DecisionNode(cond=has_special_card)
root.right.right.left  = DecisionNode(action=play_special)
root.right.right.right = DecisionNode(action=play_lowest)

# Q-Learning agent
class QLearningAgent:
    def __init__(self):
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
        # actions by index: 0=high,1=low,2=special,3=highest,4=lowest
        self.actions = ['high', 'low', 'special', 'highest', 'lowest']
        # Q-table  f(2)x h(2)x l(2)x s(2) x actions f: figure, h: high value, l: low value, s:special
        self.Q = np.zeros((2, 2, 2, 2, len(self.actions)))

    def get_state(self, figure, hand):
        f = 1 if figure >= 8 else 0
        h = 1 if any(7 <= int(card[:-1]) <= 10 for card in hand) else 0
        l = 1 if any(2 <= int(card[:-1]) <= 4  for card in hand) else 0
        s = 1 if any(card in ['2S', '9S'] for card in hand) else 0
        return (f, h, l, s)

    def choose(self, state):
        # find valid moves
        f, h, l, s = state
        valid = []
        if f:
            if h: valid.append(0)
            if s: valid.append(2)
            valid.append(3)
        else:
            if l: valid.append(1)
            if s: valid.append(2)
            valid.append(4)
        # epsilon-greedy
        if np.random.rand() < self.epsilon:
            return np.random.choice(valid)
        # greedy (:choose best action for now)
        Qval = self.Q[state]
        best = valid[0]
        for x in valid:
            if Qval[x] > Qval[best]:
                best = x
        return best

    def update(self, state, action, reward, next_state):
        # compute max next
        f, h, l, s = state
        fn, hn, ln, sn = next_state
        valid_next = []
        if fn:
            if hn: valid_next.append(0) # high
            if sn: valid_next.append(2) #special
            valid_next.append(3) #highest
        else:
            if ln: valid_next.append(1) #low
            if sn: valid_next.append(2) # special
            valid_next.append(4) #lowest
        max_next = max(self.Q[fn, hn, ln, sn, i] for i in valid_next) if valid_next else 0 # Max future Q
        current = self.Q[f, h, l, s, action]
        self.Q[f, h, l,s, action] = current + self.alpha * (reward + self.gamma * max_next - current)

    def act(self, figure, hand):
        state = self.get_state(figure, hand)
        idx = self.choose(state)
        return self.actions[idx]

    def load(self, path):
        with open(path, 'rb') as file:
            self.Q = pickle.load(file)

# Computer AI combining both logic(Tree & Q-learning)
class ComputerAI:
    def __init__(self, mode='easy', Qpath=None):
        self.mode = mode
        self.agent = QLearningAgent()
        if mode == 'hard' and Qpath:
            self.agent.load(Qpath)

    def play(self, game: Game):
        if self.mode == 'easy':  # [Easy mode] computer drews card randomly no logic
            hand = game.computer.hand
            choice = random.chocie(hand)
            game.computer.play_card(choice)
            return

        if self.mode == 'Normal': # [Normal mode] Computer uses tree data structure and decides
            node = root
            while node.action is None:
                if node.cond(game):
                    node = node.left
                else:
                    node = node.right
            node.action(game)
            return

        #[Hard Mode] Q-learning


        figure_value = game.current_figure.value
        hand = game.computer.hand
        choice = self.agent.act(figure_value, hand)
        play_choice(choice, game.computer)





