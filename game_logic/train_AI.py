import pickle
import random
from Computer_AI import QLearningAgent, play_choice
from game import Game

# train_AI.py
# This script runs Q-learning training for the ComputerAI (hard mode)

def main():
    agent = QLearningAgent()
    episodes = 50000  # number of training rounds

    wins = 0
    losses = 0
    ties = 0

    for ep in range(episodes):
        # 1) start a new game/round
        game = Game()

        # 2) get initial state: figure value and computer hand
        fv = game.current_figure.value
        hand = list(game.computer.hand)
        state = agent.get_state(fv, hand)

        # 3) choose an action index
        action_idx = agent.choose(state)
        action_name = agent.actions[action_idx]
        play_choice(action_name, game.computer)



        # 4) reward
        comp_score, player_score = game.resolve_round()
        if comp_score > player_score:
            reward = 1
            wins += 1
        elif comp_score < player_score:
            reward = -1
            losses += 1
        else:
            reward = 0
            ties += 1


        # 5) observing next state
        new_fv = game.current_figure.value
        new_hand = list(game.computer.hand)
        next_state = agent.get_state(new_fv, new_hand)

        # 6) update Q-table
        agent.update(state, action_idx, reward, next_state)

    #  save the trained Q-table for hard mode
    with open('q_table.pkl', 'wb') as file:
        pickle.dump(agent.Q, file)

    total = wins + losses + ties
    win_rate = wins / total * 100 if total > 0 else 0.0
    print(f"Training complete: {episodes} episodes. Q-table saved to q_table.pkl")
    print(f"Wins: {wins}, Losses: {losses}, Draws: {ties}")
    print(f"  Win rate: {win_rate:.2f}%")
    print("Q-table saved to q_table.pkl")


if __name__ == '__main__':
    main()

