from game_logic.deck import Deck
from game_logic.player import Player
import random # (for coin flip) / I(5662884) wrote all of the codes except def __init part(5667929 wrote that part)


class Game:
    """manages the overall game flow and logic"""

    def __init__(self):  # 5667929 wrote def __init part except self.round
        """initialize the game with a deck, two players, and a set number of rounds"""
        self.deck = Deck()
        self.players = [Player("You"), Player("Computer")] #5676101
        self.round = 0  # 5662884 
        self.total_rounds = 5  # this is new but it might make the game quicker to play (we dont need it)
        self.user_round_sum = 0
        self.computer_round_sum = 0
    def start_game(self):
        """starts the game"""
        print("Game is starting...")
        while not self.game_over():
            self.round += 1
            print(f"Round {self.round}")
            self.play_round()
        self.declare_winner()


    def play_round(self, user_card):
        """play round, both player and computer will draw card and card values will be compared"""
        card_player = self.deck.draw_card()
        card_computer = self.deck.draw_card()
        user = self.players[0] #5676101
        computer = self.players[1]

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
            print(f"This round is a tie! Deciding winner by coin flip...")
            winner = random.choice([self.player, self.computer])
            if winner is self.player:
                print(f"You win {self.round} by coin flip!")
                self.player.add_score(card_player)
            else:
                print(f"Computer wins {self.round} by coin flip!")
                self.computer.add_score(card_computer)
         # Special rule: no 3 or 10 right after using 2ofSp or 9ofSp 5676101
        if user.used_special == True and user_rank in ['3', '10']:
           raise ValueError("Error: You can't play a 3 or 10 right after using a special card like 2 of spades or 9 of spades")
            #For each round the sum of the values of the number cards played will be stored (5676101)
        rank_user = user.get_rank(user_card)
        value_user = int(rank_user)
        self.user_round_sum += value_user
        if self.user_round_sum in [12, 19]: # If statement used to check if sum is 12 or 19
           raise ValueError("You have reached an invalid card total of 12 or 19 this round.")
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




















