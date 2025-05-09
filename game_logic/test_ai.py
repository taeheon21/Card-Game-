# test_ai_interactive.py
# Console-based interactive test for ComputerAI modes
#!!! "python -m game_logic.test_ai" type this to run code in vsc terminal

import random
from .Computer_AI import ComputerAI
from .game import Game


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

    # 3) Start one Game instance so hands persist
    game = Game()
    human = game.players[0]
    computer = game.players[1]

    rounds = 15
    for rnd in range(1, rounds + 1):
        print(f"--- Round {rnd} ---")

        # draw figure card for this round
        game.current_figure = game.deck.draw_figure_card()
        fig_code, fig_val = game.current_figure
        print(f"Figure card: {fig_code} (value {fig_val})")

        # show human hand
        print("Your hand:")
        for i, c in enumerate(human.hand):
            print(f"  {i}: {c}")

        # human plays
        while True:
            sel = input(f"Choose a card index (0-{len(human.hand) - 1}): ")
            if not sel.isdigit():
                print("Enter a number.")
                continue
            idx = int(sel)
            if 0 <= idx < len(human.hand):
                human_card = human.hand[idx]
                human.play_card(human_card)
                break
            print("Index out of range.")
        print(f"You played: {human_card}")

        # show computer hand before play
        print("Computer hand before play:")
        print(", ".join(computer.hand))

        # computer plays
        before = set(computer.hand)
        ai.play(game)
        played = before - set(computer.hand)
        comp_card = played.pop() if played else None
        print(f"Computer played: {comp_card}")

        # determine winner and score assignment
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

        print(f"Scores -> You: {human.score} | Computer: {computer.score}\n")

    print(f"All {rounds} rounds completed.")
    print(f"Final Scores -> You: {human.score} | Computer: {computer.score}")


if __name__ == '__main__':
    main()
