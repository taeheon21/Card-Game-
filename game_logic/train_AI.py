

"""Q-learning training script for ComputerAI hard mode.

Runs multiple episodes to train the agent and saves the Q-table.
"""

import pickle
import random
from Computer_AI import QLearningAgent
from game import Game


def choose_card_by_action(action, hand, get_rank):
    """Select a card from hand based on the given action strategy.

    This picks from highs, mids, lows, special cards, highest, or lowest
    depending on action. If none match, it falls back to min/max or random
    
        action: one of 'high', 'mid', 'low',
            'special', 'highest', 'lowest'.
        hand : list of card codes, e.g. '10H'.
        get_rank : function that returns int rank.

    Returns:
        str: selected card code.
    """
    # high-range: ranks 7–10, pick lowest of highs if available
    if action == 'high':
        highs = sorted(
            [c for c in hand if 7 <= get_rank(c) <= 10],
            key=get_rank
        )
        return highs[0] if highs else max(hand, key=get_rank)

    # mid-range: ranks 5–7, pick lowest of mids if available
    if action == 'mid':
        mids = sorted(
            [c for c in hand if 5 <= get_rank(c) <= 7],
            key=get_rank
        )
        return mids[0] if mids else min(hand, key=get_rank)

    # low-range: ranks 2–4, pick highest of lows if available
    if action == 'low':
        lows = sorted(
            [c for c in hand if 2 <= get_rank(c) <= 4],
            key=get_rank,
            reverse=True
        )
        return lows[0] if lows else min(hand, key=get_rank)

    # special cards: 2S or 9S, else random
    if action == 'special':
        specs = [c for c in hand if c in ['2S', '9S']]
        return specs[0] if specs else random.choice(hand)

    # highest: play top-ranked card
    if action == 'highest':
        return max(hand, key=get_rank)

    # lowest: default case
    return min(hand, key=get_rank)


def main():
    """Train the Q-learning agent over multiple episodes."""
    agent = QLearningAgent()
    episodes = 50_000  # number of training rounds

    wins = 0
    losses = 0
    ties = 0

    for ep in range(episodes):
        # 1) Start a new game/round
        game = Game()
        game.current_figure = game.deck.draw_figure_card()

        player = game.players[0]
        computer = game.players[1]

        # 2) Get initial state from current figure and computer hand
        fv = game.current_figure[1]
        hand = list(computer.hand)
        state = agent.get_state(fv, hand)

        # Opponent plays a random card
        opp_card = random.choice(player.hand)
        player.play_card(opp_card)

        # 3) Agent selects action and plays corresponding card
        action_name = agent.act(fv, hand)
        comp_card = choose_card_by_action(
            action_name,
            computer.hand,
            computer.get_rank
        )
        computer.play_card(comp_card)

        # 4) Compute reward based on card comparison
        opp_val = int(opp_card[:-1])
        comp_val = int(comp_card[:-1])
        if opp_val > comp_val:
            reward = -1
            losses += 1
        elif opp_val < comp_val:
            reward = 1
            wins += 1
        else:
            # tie → random tiebreaker
            t_opp = random.choice(player.hand)
            t_comp = random.choice(computer.hand)
            if int(t_opp[:-1]) >= int(t_comp[:-1]):
                reward = -1
                losses += 1
            else:
                reward = 1
                wins += 1

        # 5) Observe next state and update Q-table
        new_fv = game.current_figure[1]
        new_hand = list(computer.hand)
        next_state = agent.get_state(new_fv, new_hand)
        agent.update(
            state,
            agent.actions.index(action_name),
            reward,
            next_state
        )

    # Save trained Q-table for 'hard' mode
    with open('q_table.pkl', 'wb') as f:
        pickle.dump(agent.Q, f)

    total = wins + losses + ties
    win_rate = wins / total * 100 if total else 0.0

    print(f"Training complete: {episodes} episodes.")
    print(f"Wins: {wins}, Losses: {losses}, Draws: {ties}")
    print(f"Win rate: {win_rate:.2f}%")
    print("Q-table saved to q_table.pkl")


if __name__ == '__main__':
    main()
