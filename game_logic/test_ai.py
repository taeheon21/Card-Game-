"""Console-based interactive test for ComputerAI in different modes.

Run with:
    python -m game_logic.test_ai
"""

import random
from .Computer_AI import ComputerAI
from .game import Game


MODE_MAP = {
    '1': 'easy',
    '2': 'normal',
    '3': 'hard',
}


def main():
    """Play a 15‐round console game between human and ComputerAI."""
    # Select AI mode
    print("Select AI mode:")
    print("1: easy (random)")
    print("2: normal (rule tree)")
    print("3: hard (Q-learning)")
    choice = input("Enter 1/2/3: ")
    mode = MODE_MAP.get(choice, 'easy')
    print(f"Running in {mode} mode")

    # Load Q-learning AI only in hard mode
    qpath = 'q_table.pkl' if mode == 'hard' else None
    ai = ComputerAI(mode=mode, Qpath=qpath)

    # Start Game. And identify who's player
    game = Game()
    human = game.players[0]
    computer = game.players[1]

    rounds = 15
    for rnd in range(1, rounds + 1):
        print(f"--- Round {rnd} ---")

        # Draw and announce the figure card for this round
        game.current_figure = game.deck.draw_figure_card()
        fig_code, fig_val = game.current_figure
        print(f"Figure card: {fig_code} (value {fig_val})\n")

        # Display human player's hand 
        print("Your hand:")
        for i, card in enumerate(human.hand):
            print(f"  {i}: {card}")

        # human plays
        while True:
            sel = input(f"Choose a card index (0-{len(human.hand)-1}): ")
            if not sel.isdigit():
                print("Enter a number.")
                continue
            idx = int(sel)
            if 0 <= idx < len(human.hand):
                human_card = human.hand[idx]
                human.play_card(human_card)
                break
            print("Index out of range.")
        print(f"\nYou played: {human_card}\n")

        # Show computer's remaining hand before AI decision, so I can judge wheather AI's decision is correct.
        print("Computer hand before play:")
        print(", ".join(computer.hand))

        # AI plays one card based on selected mode
        before = set(computer.hand)
        ai.play(game)
        played = before - set(computer.hand)
        comp_card = played.pop() if played else None
        print(f"Computer played: {comp_card}\n")

        # Determine round winner and update scores
        hnum = int(human_card[:-1])
        cnum = int(comp_card[:-1])
        if hnum > cnum:
            print(">>> You win this round!")
            human.score += fig_val
        elif hnum < cnum:
            print(">>> Computer wins this round.")
            computer.score += fig_val
        else:
            print(">>> It's a tie! (no figure awarded)")

        # Display updated scores
        print(f"\nScores -> You: {human.score} | "
              f"Computer: {computer.score}\n")

    # End of all rounds
    print(f"All {rounds} rounds completed.")
    print(f"Final Scores -> You: {human.score} | Computer: "
          f"{computer.score}")


if __name__ == '__main__':
    main()
