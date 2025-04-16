from game_logic.deck import Deck
from game_logic.player import Player
import random # (for coin flip)


class Game:
    """manages the overall game flow and logic"""

    def __init__(self):
        """initialize the game with a deck, two players, and a set number of rounds"""
        self.deck = Deck()
        self.player = Player("you")
        self.computer = Player("computer")
        self.round = 0
        self.total_rounds = 5  # this is new but it might make the game quicker to play (we dont need it)

    def start_game(self):
        """starts the game"""
        print("Game is starting...")
        while self.round <= self.total_rounds:  # I can change it to def game_over if we won't select total round
            self.round += 1
            print(f"Round {self.round}")
            self.play_round()
        self.declare_winner()




    def play_round(self):
        """play round, both player and computer will draw card and card values will be compared"""
        card_player = self.deck.draw_card()
        card_computer = self.deck.draw_card()

        #If there is no card anymore
        if card_player is None or card_computer is None:
            print("There's no card to draw")
            return

        print(f"You played: {card_player}")
        print(f"Computer played: {card_computer}")

        # Comparing number
        if card_player > card_computer:
            print(f"You win {self.round}!")
            self.player.add_score(card_player)
        elif card_computer > card_player:
            print(f"Computer win {self.round}!")
            self.computer.add_score(card_computer)
        # flip coin(else) I  use random I could make flip coin to decide winner.
        else:
            print(f"This round is tie! Deciding winner by coin flip...")
            winner = random.choice([self.player, self.computer])
            if winner is self.player:
                print(f"You win {self.round} by coin flip!")
                self.player.add_score(card_player)
            else:
                print(f"Computer wins {self.round} by coin flip!")
                self.computer.add_score(card_computer)


    def game_over(self):
        """check if game completion conditions are satisfied(round expired or deck is empty)"""
        return self.round >= self.total_rounds or self.deck.is_empty()


    def declare_winner(self):
        """ declare final winner"""
        print("Game Over!")
        print(f"Your score is {self.player.score}")
        print(f"Computer score is {self.computer.score}")
        if self.player.score > self.computer.score:
            print(f"Congratulations! You win the Game!!")
        elif self.player.score < self.computer.score:
            print(f"Computer wins the game")
    """ else:
            print(f"This round is tie! Deciding winner by coin flip...")  If we have total 5 rounds I think this codes are unnecessary"""




















