import pickle
import random
import numpy as np
from .game import Game


class DecisionNode:
    """Decision tree node for game AI."""

    def __init__(self, cond=None, action=None):
        """ cond: to judge, action: to act """
        self.cond = cond
        self.action = action
        self.left = None   # when condition is True
        self.right = None  # when condition is False


def is_figure_high(game):
    """Return True if current figure value is at least 8."""
    return game.current_figure[1] >= 8


def is_figure_mid(game):
    """Return True if current figure value is between 5 and 8."""
    v = game.current_figure[1]
    return 5 <= v <= 8


def has_high_cards(game):
    """Return True if computer has any card with rank 7–10.
    c[:-1] strips the suit letter, leaving the numeric rank as string"""
    for c in game.computer.hand:
        if 7 <= int(c[:-1]) <= 10:
            return True
    return False


def has_mid_cards(game):
    """Return True if player 1 has any card with rank 5–7."""
    for c in game.players[1].hand:
        if 5 <= int(c[:-1]) <= 7:
            return True
    return False


def has_low_cards(game):
    """Return True if computer has any card with rank 2–4."""
    for c in game.computer.hand:
        if 2 <= int(c[:-1]) <= 4:
            return True
    return False


def has_special_card(game):
    """Return True if computer has a special card (2S or 9S)."""
    for c in game.computer.hand:
        if c in ['2S', '9S']:
            return True
    return False


def play_high_val(game):
    """Play a high-value card (7–10) if available."""
    return play_choice('high', game.computer)


def play_mid_val(game):
    """Play a mid-value card (5–7) if available."""
    return play_choice('mid', game.computer)


def play_low_val(game):
    """Play a low-value card (2–4) if available."""
    return play_choice('low', game.computer)


def play_special(game):
    """Play a special card (2S or 9S) if available."""
    return play_choice('special', game.computer)


def play_highest(game):
    """Play the highest-value card."""
    return play_choice('highest', game.computer)


def play_lowest(game):
    """Play the lowest value card."""
    return play_choice('lowest', game.computer)


def play_choice(choice, player):
    """Play card based on tree logic.
     We define get_num as a lambda to extract the numeric rank from a card string.
     Using a lambda here avoids repeating int(c[:-1]) everywhere."""
    hand = player.hand
    get_num = lambda c: int(player.get_rank(c))

    if choice == 'high':
        # select first 7–10, else highest
        highs = [c for c in hand if 7 <= get_num(c) <= 10]
        card = highs[0] if highs else max(hand, key=get_num)
    elif choice == 'mid':
        # select first 5–7, else lowest
        mids = [c for c in hand if 5 <= get_num(c) <= 7]
        card = mids[0] if mids else min(hand, key=get_num)
    elif choice == 'low':
        # select first 2–4, else lowest
        lows = [c for c in hand if 2 <= get_num(c) <= 4]
        card = lows[0] if lows else min(hand, key=get_num)
    elif choice == 'special':
        # select special, else random
        specials = [c for c in hand if c in ['2S', '9S']]
        card = specials[0] if specials else random.choice(hand)
    elif choice == 'highest':
        card = max(hand, key=get_num)
    else:
        # 'lowest'
        card = min(hand, key=get_num)

    player.play_card(card)
    return card  # UI return the card played


# Build the decision tree
root = DecisionNode(cond=is_figure_high)
root.left = DecisionNode(cond=has_high_cards)
root.left.left = DecisionNode(action=play_high_val)
root.left.right = DecisionNode(cond=has_special_card)
root.left.right.left = DecisionNode(action=play_special)
root.left.right.right = DecisionNode(action=play_highest)

root.right = DecisionNode(cond=is_figure_mid)
root.right.left = DecisionNode(cond=has_mid_cards)
root.right.left.left = DecisionNode(action=play_mid_val)
root.right.left.right = DecisionNode(cond=has_special_card)
root.right.left.right.left = DecisionNode(action=play_special)
root.right.left.right.right = DecisionNode(action=play_highest)

root.right.right = DecisionNode(cond=has_low_cards)
root.right.right.left = DecisionNode(action=play_low_val)
root.right.right.right = DecisionNode(cond=has_special_card)
root.right.right.right.left = DecisionNode(action=play_special)
root.right.right.right.right = DecisionNode(action=play_lowest)


class QLearningAgent:
    """Q-learning agent for card playing."""

    def __init__(self):
        """Initialize learning rates, action space, and Q-table."""
        self.alpha = 0.1 # α (alpha): learning rate controls how quickly new experiences override old Q-values
        self.gamma = 0.9 # γ (gamma): discount factor determines how much future rewards count
        self.epsilon = 0.1 # ε (epsilon): exploration rate for ε-greedy policy
        self.actions = [
            'high', 'mid', 'low', 'special', 'highest', 'lowest'  
        ]  # Define possible actions
        # dimensions: figure×has_high×has_mid×has_low×has_special×actions
        self.Q = np.zeros((3, 2, 2, 2, 2, len(self.actions)))

    def get_state(self, figure, hand):
        """Map (figure, hand) to dicrete state tuple."""
        f = 2 if figure >= 8 else (1 if figure >= 5 else 0)
        h = int(any(7 <= int(c[:-1]) <= 10 for c in hand))
        m = int(any(5 <= int(c[:-1]) <= 7 for c in hand))
        l = int(any(2 <= int(c[:-1]) <= 4 for c in hand))
        s = int(any(c in ['2S', '9S'] for c in hand))
        return (f, h, m, l, s)

    def valid_actions(self, state):
        """Return list of valid action index for given state."""
        f, h, m, l, s = state
        valid = []
        if f == 2:
            if h:
                valid.append(self.actions.index('high'))
            if s:
                valid.append(self.actions.index('special'))
            valid.append(self.actions.index('highest'))
        elif f == 1:
            if m:
                valid.append(self.actions.index('mid'))
            if s:
                valid.append(self.actions.index('special'))
            valid.append(self.actions.index('lowest'))
        else:
            if l:
                valid.append(self.actions.index('low'))
            if s:
                valid.append(self.actions.index('special'))
            valid.append(self.actions.index('lowest'))
        return valid

    def choose(self, state):
        """Choose an action via ε-greedy policy."""
        valid = self.valid_actions(state)
        if random.random() < self.epsilon:
            return random.choice(valid)
        q_vals = self.Q[state]
        best = valid[0]
        for a in valid:
            if q_vals[a] > q_vals[best]:
                best = a
        return best

    def update(self, state, action, reward, next_state):
        """Update Q-table using the Bellman equation."""
        valid_next = self.valid_actions(next_state)
        max_next = (max(self.Q[next_state][i] for i in valid_next)
                    if valid_next else 0)
        f, h, m, l, s = state
        current = self.Q[f, h, m, l, s, action]
        self.Q[f, h, m, l, s, action] = (
            current + self.alpha *
            (reward + self.gamma * max_next - current)
        )

    def act(self, figure, hand):
        """Return action name for given figure and hand."""
        state = self.get_state(figure, hand)
        idx = self.choose(state)
        return self.actions[idx]

    def load(self, path):
        """Load Q-table from pickle file at given path. It's hard to run AI code during the game process, so I decided to load the AI file"""
        with open(path, 'rb') as file:
            self.Q = pickle.load(file)


class ComputerAI:
    """Computer player AI with easy, normal, hard modes."""

    def __init__(self, mode='easy', Qpath=None):
        """Set mode and optionally load Q-learning data."""
        self.mode = mode
        self.agent = QLearningAgent()
        if mode == 'hard' and Qpath:
            self.agent.load(Qpath)

    def play(self, game: Game):
        """Play one card according to selected mode and return it."""
        mode = self.mode.lower()
        comp = game.players[1]

        if mode == 'easy':  # random draw, no logic
            card = random.choice(comp.hand)
            comp.play_card(card)
            return card

        elif mode == 'normal':  # use decision tree logic
            node = root
            while node.action is None:
                node = node.left if node.cond(game) else node.right
            card = node.action(game)
            return card

        elif mode == 'hard':
            # Q-learning based decision
            fv = game.current_figure[1]
            choice = self.agent.act(fv, comp.hand)
            card = play_choice(choice, comp)
            return card

        else:
            raise ValueError(f'Wrong mode selection: {mode}')
