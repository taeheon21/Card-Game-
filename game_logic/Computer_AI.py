import pickle
import random
import numpy as np
from game import Game





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

def is_figure_mid(game):
    v = game.current_figure.value
    return 5 <= v <= 8


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

def play_mid_val(game):
    play_choice('mid', game.computer)



def play_low_val(game):
    play_choice('low', game.computer)


def play_special(game):
    play_choice('special', game.computer)



def play_highest(game):
    play_choice('highest', game.computer)




def play_lowest(game):
    play_choice('lowest', game.computer)



def play_choice(choice, player):
    hand = player.hand

    get_num = lambda c: int(player.get_rank(c))

    if choice == 'high':
        # 7~10
        highs = [c for c in hand if 7 <= get_num(c) <= 10]
        card = highs[0] if highs else max(hand, key=get_num)
    elif choice == 'mid':
        mids = [c for c in hand if 5 <= get_num(c) <= 7]

        card = mids[0] if mids else min (hand, key=get_num)

    elif choice == 'low':
        # 2~4
        lows = [c for c in hand if 2 <= get_num(c) <= 4]
        card = lows[0] if lows else min(hand, key=get_num)
    elif choice == 'special':
        #
        specs = [c for c in hand if c in ['2S','9S']]
        card = specs[0] if specs else random.choice(hand)
    elif choice == 'highest':

        card = max(hand, key=get_num)
    else:  # 'lowest'

        card = min(hand, key=get_num)

    player.play_card(card)




# Build the decision tree
root = DecisionNode(cond=is_figure_high)
# figure>=8
root.left = DecisionNode(cond=has_high_cards)
root.left.left  = DecisionNode(action=play_high_val)
root.left.right = DecisionNode(cond=has_special_card)
root.left.right.left  = DecisionNode(action=play_special)
root.left.right.right = DecisionNode(action=play_highest)
# figure = mid
root.right = DecisionNode(cond=is_figure_mid)
root.right.left = DecisionNode(cond=has_mid_cards)
root.right.left.left  = DecisionNode(action=play_mid_val)
root.right.left.right = DecisionNode(cond=has_special_card)
root.right.left.right.left  = DecisionNode(action=play_special)
root.right.left.right.right = DecisionNode(action=play_highest)

# figure<mid
root.right.right = DecisionNode(cond=has_low_cards)
root.right.right.left  = DecisionNode(action=play_low_val)
root.right.right.right = DecisionNode(cond=has_special_card)
root.right.right.right.left  = DecisionNode(action=play_special)
root.right.right.right.right = DecisionNode(action=play_lowest)

# Q-Learning agent
class QLearningAgent:
    def __init__(self):
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
        # actions by index: 0=high,1=low,2=special,3=highest,4=lowest
        self.actions = ['high', 'mid' , 'low', 'special', 'highest', 'lowest']
        # Q-table  f(2)x h(2)x l(2)x s(2) x actions f: figure, h: high value, l: low value, s:special
        self.Q = np.zeros((3, 2, 2, 2, len(self.actions)))

    def get_state(self, figure, hand):
        f = 2 if figure >= 8 else (1 if figure >=5 else 0)
        h = 1 if any(7 <= int(card[:-1]) <= 10 for card in hand) else 0
        m = 1 if any(5 <= int(card[:-1]) <= 7  for card in hand) else 0
        l = 1 if any(2 <= int(card[:-1]) <= 4  for card in hand) else 0
        s = 1 if any(card in ['2S', '9S'] for card in hand) else 0
        return (f, h, m, l, s)

    def legal_actions(self, state):
        f, h, m, l, s = state
        valid = []
        if f == 2:
            if h: valid.append(self.actions.index('high'))
            if s: valid.append(self.actions.index('special'))
            valid.append(self.actions.index('highest'))
        elif f == 1:
            if m: valid.append(self.actions.index('mid'))
            if s: valid.append(self.actions.index('special'))
            valid.append(self.actions.index('lowest'))
        else:
            if l: valid.append(self.actions.index('low'))
            if s: valid.append(self.actions.index('special'))
            valid.append(self.actions.index('lowest'))
        return valid

    def choose(self, state):
        valid = self.legal_actions(state)
        if random.random() < self.epsilon:
            return random.choice(valid)
        qvals = self.Q[state]
        best = valid[0]
        for a in valid:
            if qvals[a] > qvals[best]: best = a
        return best

    def update(self, state, action, reward, next_state):
        valid_next = self.legal_actions(next_state)
        max_next = max(self.Q[next_state][i] for i in valid_next) if valid_next else 0
        f, h, m, l, s = state
        current = self.Q[f, h, m, l, s, action]
        self.Q[f, h, m, l, s, action] = current + self.alpha * (reward + self.gamma * max_next - current)

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
        comp = game.players[1]

        if self.mode == 'easy':  # [Easy mode] computer drews card randomly no logic
            card = random.choice(comp.hand)
            comp.play_card(card)
            return

        if self.mode == 'Normal': # [Normal mode] Computer uses tree data structure and decides
            node = root
            while node.action is None:
                node = node.left if node.cond(game) else node.right
            node.action(game)
            return


        #[Hard Mode] Q-learning

        fv = game.current_figure[1]
        hand = comp.hand
        choice = self.agent.act(fv, hand)
        play_choice(choice, comp)








