# test_ai_modes.py
# Basic test harness for ComputerAI in easy/normal/hard modes

from Computer_AI import ComputerAI
from game import Game
import random


def simulate_mode(mode, rounds=5, qpath='q_table.pkl'):
    print(f"=== Testing mode: {mode} ===")
    # Load Q-table for hard mode
    ai = ComputerAI(mode=mode, Qpath=qpath if mode=='hard' else None)
    for i in range(1, rounds+1):
        # Initialize a fresh game
        game = Game()
        # Draw figure card for this round
        game.current_figure = game.deck.draw_figure_card()
        comp = game.playerss[1]

        # Capture hand before play
        hand_before = list(comp.hand)
        # AI makes its move
        ai.play(game)
        # Determine which card was played
        played = set(hand_before) - set(comp.hand)
        card_played = played.pop() if played else None

        print(f"Round {i}: Figure={game.current_figure[1]}, Played => {card_played}")
    print()


def main():
    # Run basic tests for each mode
    for mode in ['easy', 'normal', 'hard']:
        simulate_mode(mode)


if __name__ == '__main__':
    main()
