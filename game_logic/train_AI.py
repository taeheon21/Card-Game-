import pickle
import random
from Computer_AI import QLearningAgent, play_choice
from game import Game

# train_AI.py
# This script runs Q-learning training for the ComputerAI (hard mode)

def choose_card_by_action(action, hand, get_rank):

    if action == 'high':
        highs = [c for c in hand if 7 <= get_rank(c) <= 10]
        return highs[0] if highs else max(hand, key=get_rank)
    if action == 'low':
        lows = [c for c in hand if 2 <= get_rank(c) <= 4]
        return lows[0] if lows else min(hand, key=get_rank)
    if action == 'special':
        specs = [c for c in hand if c in ['2S','9S']]
        return specs[0] if specs else random.choice(hand)
    if action == 'highest':
        return max(hand, key=get_rank)
    # lowest
    return min(hand, key=get_rank)

def main():
    agent = QLearningAgent()
    episodes = 50000  # number of training rounds

    wins = 0
    losses = 0
    ties = 0

    for ep in range(episodes):
        # 1) start a new game/round
        game = Game()
        game.current_figure = game.deck.draw_figure_card()

        player = game.players[0]

        computer = game.players[1]

        # 2) get initial state: figure value and computer hand
        fv = game.current_figure[1]
        hand = list(computer.hand)
        state = agent.get_state(fv, hand)
        #
        opp_card = random.choice(player.hand)
        player.play_card(opp_card)

        # 3) choose an action index
        action_name = agent.act(fv, hand)
        comp_card = choose_card_by_action(action_name,
                                          computer.hand,
                                          player.get_rank)
        computer.play_card(comp_card)


        # 4) play the round and compute reward based on score changes
        opp_num = int(opp_card[:-1])
        comp_num = int(comp_card[:-1])
        if opp_num > comp_num:
            reward = -1
            losses += 1
        elif opp_num < comp_num:
            reward = 1
            wins += 1
        else:
            # tie -> random
            tie_opp = random.choice(player.hand)
            tie_comp = random.choice(computer.hand)
            if int(tie_opp[:-1]) >= int(tie_comp[:-1]):
                reward = -1
                losses += 1
            else:
                reward = 1
                wins += 1


        # 5) observing next state
        new_fv = game.current_figure[1]
        new_hand = list(computer.hand)
        next_state = agent.get_state(new_fv, new_hand)

        # 6) update Q-table
        agent.update(state, agent.actions.index(action_name), reward, next_state)

    #  save the trained Q-table for hard mode
    with open('q_table.pkl', 'wb') as file:
        pickle.dump(agent.Q, file)

    total = wins + losses + ties

    print(f"Training complete: {episodes} episodes. Q-table saved to q_table.pkl")
    print(f"Wins: {wins}, Losses: {losses}, Draws: {ties}")
    print(f"Win rate: {wins/total*100:.2f}%")
    print("Q-table saved to q_table.pkl")


if __name__ == '__main__':
    main()
