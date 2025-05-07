import pickle
import numpy as np
from game import Game
from deck import Card

# Simple decision tree nodes
class Node:
    pass

class DecisionNode(Node):
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


# Action helpers

def play_high_val(game):
    game.computer.play_high_value_card()


def play_low_val(game):
    game.computer.play_low_value_card()


def play_special(game):
    game.computer.play_special_card()


def play_highest(game):
    game.computer.play_highest_value_card()


def play_lowest(game):
    game.computer.play_lowest_value_card()

# Build the decision tree
root = Node(cond=is_figure_high)
# figure>=8
root.left = Node(cond=has_high_cards)
root.left.left  = Node(action=play_high)
root.left.right = Node(cond=has_special_card)
root.left.right.left  = Node(action=play_special)
root.left.right.right = Node(action=play_highest)
# figure<8
root.right = Node(cond=has_low_cards)
root.right.left  = Node(action=play_low)
root.right.right = Node(cond=has_special_card)
root.right.right.left  = Node(action=play_special)
root.right.right.right = Node(action=play_lowest)

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
        h = 1 if any(7 <= c.value <= 10 for c in hand) else 0
        l = 1 if any(2 <= c.value <= 4 for c in hand) else 0
        s = 1 if any(c.code in ['2S', '9S'] for c in hand) else 0
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
        with open(path, 'rb') as f:
            self.Q = pickle.load(f)

# Computer AI combining both logic(Tree & Q-learning)
class ComputerAI:
    def __init__(self, mode='easy', qpath=None):
        self.mode = mode

        self.agent = QLearningAgent()
        if mode in ['normal', 'hard'] and qpath:
            self.agent.load(qpath)

    def play(self, game):
        if self.mode == 'easy':
            node = root
            while node.action is None:
                if node.cond(game):
                    node = node.left
                else:
                    node = node.right
            node.action(game)
            return

