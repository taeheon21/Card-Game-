import pickle
import random
import numpy as np
from game import Game

# --- Action helper for Q/hard mode ---
def choose_card_by_action(action, hand, get_rank):
    # get_rank: function(card)->int
    if action == 'high':
        # play smallest card in 7-10
        highs = sorted([c for c in hand if 7 <= get_rank(c) <= 10], key=get_rank)
        return highs[0] if highs else max(hand, key=get_rank)
    if action == 'mid':
        # play smallest card in 5-7
        mids = sorted([c for c in hand if 5 <= get_rank(c) <= 7], key=get_rank)
        return mids[0] if mids else min(hand, key=get_rank)
    if action == 'low':
        # play largest card in 2-4
        lows = sorted([c for c in hand if 2 <= get_rank(c) <= 4], key=get_rank, reverse=True)
        return lows[0] if lows else min(hand, key=get_rank)
    if action == 'special':
        # use special only if figure >4 or only card
        specs = [c for c in hand if c.code in ['2S','9S']]
        return specs[0] if specs else random.choice(hand)
    if action == 'highest':
        return max(hand, key=get_rank)
    # 'lowest'
    return min(hand, key=get_rank)

# --- Decision tree for normal mode ---
class DecisionNode:
    def __init__(self, cond=None, action=None):
        self.cond = cond       # function(game)->bool
        self.action = action   # function(game)->None
        self.left = None
        self.right = None

# Conditions

def is_figure_high(game):
    return game.current_figure.value >= 8


def is_figure_mid(game):
    fv = game.current_figure.value
    return 5 <= fv < 8


def has_high_cards(game):
    return any(7 <= c.value <= 10 for c in game.players[1].hand)


def has_mid_cards(game):

    for c in game.computer.hand:
        if 5 <= c.value <= 7:
            return True
    return False


def has_low_cards(game):
    return any(2 <= c.value <= 4 for c in game.players[1].hand)


def has_special_card(game):
    # preserve special if figure <=4 and hand>1
    specs = [c for c in game.players[1].hand if c.code in ['2S','9S']]
    if not specs:
        return False
    return game.current_figure.value > 4 or len(game.players[1].hand) == 1

# Actions for tree mode

def play_high_val(game):
    comp = game.players[1]
    card = choose_card_by_action('high', comp.hand, comp.get_rank)
    comp.play_card(card)


def play_mid_val(game):
    comp = game.players[1]
    card = choose_card_by_action('mid', comp.hand, comp.get_rank)
    comp.play_card(card)


def play_low_val(game):
    comp = game.players[1]
    card = choose_card_by_action('low', comp.hand, comp.get_rank)
    comp.play_card(card)


def play_special(game):
    comp = game.players[1]
    card = choose_card_by_action('special', comp.hand, comp.get_rank)
    comp.play_card(card)


def play_highest(game):
    comp = game.players[1]
    card = choose_card_by_action('highest', comp.hand, comp.get_rank)
    comp.play_card(card)


def play_lowest(game):
    comp = game.players[1]
    card = choose_card_by_action('lowest', comp.hand, comp.get_rank)
    comp.play_card(card)

# Build the decision tree
root = DecisionNode(cond=is_figure_high)
# High branch
root.left = DecisionNode(cond=has_high_cards)
root.left.left = DecisionNode(action=play_high_val)
root.left.right = DecisionNode(cond=has_special_card)
root.left.right.left = DecisionNode(action=play_special)
root.left.right.right = DecisionNode(action=play_highest)
# Not high -> mid/low split
root.right = DecisionNode(cond=is_figure_mid)
# Mid branch: 5<=fig<8
root.right.left = DecisionNode(action=play_mid_val)
# Not mid -> low branch
root.right.right = DecisionNode(cond=has_low_cards)
root.right.right.left = DecisionNode(action=play_low_val)
root.right.right.right = DecisionNode(cond=has_special_card)
root.right.right.right.left = DecisionNode(action=play_special)
root.right.right.right.right = DecisionNode(action=play_lowest)

# --- Q-Learning agent ---
class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = ['high', 'mid', 'low', 'special', 'highest', 'lowest']
        self.Q = np.zeros((3,2,2,2,len(self.actions)))

    def get_state(self, figure, hand):
        if figure >= 8:
            f = 0
        elif figure >= 5:
            f = 1
        else:
            f = 2
        h = int(any(7 <= c.value <= 10 for c in hand))
        l = int(any(2 <= c.value <= 4 for c in hand))
        s = int(any(c.code in ['2S','9S'] for c in hand))
        return (f, h, l, s)

    def legal_actions(self, state):
        f, h, l, s = state
        legal = []
        if f == 0:  # high figure
            if h: legal.append(self.actions.index('high'))
            if s: legal.append(self.actions.index('special'))
            legal.append(self.actions.index('highest'))
        elif f == 1:  # mid figure
            legal.append(self.actions.index('mid'))
        else:  # low figure
            if l: legal.append(self.actions.index('low'))
            if s: legal.append(self.actions.index('special'))
            legal.append(self.actions.index('lowest'))
        return legal

    def choose(self, state):
        legal = self.legal_actions(state)
        if random.random() < self.epsilon:
            return random.choice(legal)
        qvals = self.Q[state]
        # select best legal
        best = legal[0]
        for a in legal:
            if qvals[a] > qvals[best]: best = a
        return best

    def update(self, state, action, reward, next_state):
        f, h, l, s = state
        legal_next = self.legal_actions(next_state)
        max_next = max(self.Q[next_state][i] for i in legal_next) if legal_next else 0
        cur = self.Q[f, h, l, s, action]
        self.Q[f, h, l, s, action] = cur + self.alpha * (reward + self.gamma * max_next - cur)

    def act(self, figure, hand):
        state = self.get_state(figure, hand)
        idx = self.choose(state)
        return self.actions[idx]

    def load(self, path=None):
        if path:
            with open(path, 'rb') as f:
                self.Q = pickle.load(f)

# --- Computer AI facade ---
class ComputerAI:
    def __init__(self, mode='easy', Qpath=None):
        self.mode = mode.lower()
        self.agent = QLearningAgent()
        if self.mode == 'hard' and Qpath:
            self.agent.load(Qpath)

    def play(self, game: Game):
        comp = game.players[1]
        if self.mode == 'easy':
            # random
            card = random.choice(comp.hand)
            comp.play_card(card)
            return
        if self.mode == 'normal':
            node = root
            while node.action is None:
                node = node.left if node.cond(game) else node.right
            node.action(game)
            return
        # hard
        fv = game.current_figure.value
        hand = comp.hand
        action = self.agent.act(fv, hand)
        card = choose_card_by_action(action, hand, comp.get_rank)
        comp.play_card(card)
