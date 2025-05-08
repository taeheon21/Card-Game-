# test_ai_interactive.py
# Console-based interactive test for ComputerAI modes

import random
from Computer_AI import ComputerAI
from game import Game

MODE_MAP = {'1': 'easy', '2': 'normal', '3': 'hard'}

def main():
    # Select mode
    print("Select AI mode:")
    print("1: easy (random)")
    print("2: normal (rule tree)")
    print("3: hard (Q-learning)")
    choice = input("Enter 1/2/3: ")
    mode = MODE_MAP.get(choice, 'easy')
    print(f"Running in {mode} mode")

    # Load AI
    qpath = 'q_table.pkl' if mode == 'hard' else None
    ai = ComputerAI(mode=mode, Qpath=qpath)

    # Play 5 rounds
    for rnd in range(1, 6):
        print(f"\n--- Round {rnd} ---")
        game = Game()
        # Draw figure card
        game.current_figure = game.deck.draw_figure_card()

        human = game.players[0]
        comp = game.players[1]

        # Show state
        fig_code, fig_val = game.current_figure
        print(f"Figure card on the table: {fig_code} (value {fig_val})")
        print("Your hand:")
        for idx, card in enumerate(human.hand):
            print(f"{idx}: {card}")

        # Human play
        while True:
            sel = input(f"Choose a card index (0-{len(human.hand)-1}): ")
            if not sel.isdigit():
                print("Please enter a number.")
                continue
            idx = int(sel)
            if 0 <= idx < len(human.hand):
                human_card = human.hand[idx]
                human.play_card(human_card)
                break
            else:
                print("Index out of range.")

        print(f"You played: {human_card}")

        # Computer play
        # Show computer's hand before its move
        print("Computer hand:", ", ".join(comp.hand))
        before = set(comp.hand)
        ai.play(game)
        played = before - set(comp.hand)
        comp_card = played.pop() if played else None
        print(f"Computer played: {comp_card}")

        # Determine winner
        hnum = int(human_card[:-1])
        cnum = int(comp_card[:-1])
        if hnum > cnum:
            print("You win this round!")
        elif hnum < cnum:
            print("Computer wins this round.")
        else:
            print("It's a tie!")

    print("\nAll rounds completed.")

if __name__ == '__main__':
    main()
