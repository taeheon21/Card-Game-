# test_tree.py
# Basic tests for the Decision Tree in Computer_AI.py (normal mode)

from Computer_AI import root, play_high_val, play_low_val, play_special, play_highest, play_lowest

# Dummy classes to simulate Game and Player
class DummyPlayer:
    def __init__(self, hand):
        self.hand = hand
        self.actions = []
    def play_high_value_card(self):
        self.actions.append('play_high_value_card')
    def play_low_value_card(self):
        self.actions.append('play_low_value_card')
    def play_special_card(self):
        self.actions.append('play_special_card')
    def play_highest_value_card(self):
        self.actions.append('play_highest_value_card')
    def play_lowest_value_card(self):
        self.actions.append('play_lowest_value_card')

class DummyGame:
    def __init__(self, figure_value, hand):
        # current_figure is stored as (code, value)
        self.current_figure = ('X', figure_value)
        # index 1 is computer
        self.players = [None, DummyPlayer(hand)]
    @property
    def computer(self):
        return self.players[1]

# Helper to traverse the tree and execute the action
def run_tree(game):
    node = root
    while node.action is None:
        if node.cond(game):
            node = node.left
        else:
            node = node.right
    node.action(game)
    return game.computer.actions[-1]

# Test cases: tuple of (figure_value, hand, expected_action_method_name)
tests = [
    (9, ['7H','5D'], 'play_high_value_card'),          # figure>=8, has high
    (9, [], 'play_highest_value_card'),                 # figure>=8, no high, no special
    (9, ['2S'], 'play_special_card'),                   # figure>=8, no high, has special
    (5, ['3H','8D'], 'play_low_value_card'),            # figure<8, has low
    (5, [], 'play_lowest_value_card'),                  # figure<8, no low, no special
    (5, ['9S'], 'play_special_card'),                   # figure<8, no low, has special
]

if __name__ == '__main__':
    for fv, hand, expected in tests:
        game = DummyGame(fv, hand)
        result = run_tree(game)
        assert result == expected, f"Test failed: FV={fv}, hand={hand}, got {result}, expected {expected}"
        print(f"Passed: FV={fv}, hand={hand} -> {result}")
    print("All decision-tree tests passed!")
