from game_logic.deck import Deck
from game_logic.Player import Player
import random # (for coin flip) / I(5662884) wrote all of the codes except def __init part(5667929 wrote that part)

#5676101, I've just completely rewritten most of the code to fix some issues and maintain clarity
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
        self.deal_cards()
        
    def start_game(self):
        """starts the game"""
        print("Game is starting...")
        while not self.game_over():
            self.round += 1
            print(f"Round {self.round}")
            self.play_round()
        self.declare_winner()

    def deal_cards(self): #5676101 (Distributed randomly, have to think how to distribute according to rules)
        number_deck = self.deck.create_number_cards()
        self.players[0].hand == number_deck[:18] #First 18 cards go to user
        self.players[1].hand == number_deck[18:] #Last 18 go to computer
        
    def play_round(self):
        """play round, both player and computer will draw card and card values will be compared"""
        self.user_round_sum = 0
        self.computer_round_sum = 0
        user_card = user.hand.pop(0)
        computer_card = computer.hand.pop(0)
        user = self.players[0] #5676101
        computer = self.players[1]
        rank_user = user.get_rank(user_card)
        rank_computer = computer.get_rank(computer_card)
        #The figure cards being drawn 5676101
        figure_deck = self.deck.create_figure_cards()
        if not figure_deck:
            print("All figure cards have been exhausted!")
            return
        self.current_figure = figure_deck.popleft() #5676101
        figure_id = self.current_figure[0] #5676101
        figure_value = self.current_figure[1] #5676101
        print(f"Figure card on the table: {figure_id} (worth {figure_value} points)")
        #If there is no card anymore
        if user_card is None or computer_card is None:
            print("There's no card to draw")
            return

        print(f"You played: {user_card}")
        print(f"Computer played: {computer_card}")
        #Enforcing the 2 of Spades and 9 of Spades rule (5676101)
        if user_card == '2S' or user_card == '9S':
            user.used_special = True
            user.last_special = user_card
        else:
            user.used_special = False
         # Special rule: no 3 or 10 right after using 2ofSp or 9ofSp 5676101
        if user.used_special == True and rank_user in ['3', '10']:
           raise ValueError("Error: You can't play a 3 or 10 right after using a special card like 2 of spades or 9 of spades")
        #For each round the sum of the values of the number cards played will be stored (5676101)
        value_user = int(rank_user)
        self.user_round_sum += value_user
        if self.user_round_sum in [12, 19]: # If statement used to check if sum is 12 or 19 for player
           raise ValueError("Error: The sum of your played cards cannot be 12 or 19")
        value_computer = int(rank_computer)
        self.computer_round_sum += value_computer
        if self.computer_round_sum in [12, 19]:
            raise ValueError("I think a statement isn't needed here")
        for player in self.players: #Sum of 91 exception (5676101)
            if player.score >= 91:
                print(f"{player.name} wins with 91 points!")
        # Comparing number
        if value_user > value_computer:
            print("You win this round!")
            user.add_score(figure_value)
        elif value_user < value_computer:
            print("Computer wins this round!")
            computer.add_score(figure_value)
        # flip coin(else) I  use random I could make flip coin to decide winner.
        else:
            print(f"This round is a tie! Deciding winner by coin flip...")
            winner = random.choice([self.players[0], self.players[1]])
            winner.add_score(figure_value)  
            print(f"{winner.name} wins the round by coin flip!")
    def game_over(self):
        """check if game completion conditions are satisfied(round expired or deck is empty)"""
        return self.round >= self.total_rounds or self.deck.is_empty()


    def declare_winner(self):
        """ declare final winner"""
        print("Game Over!")
        print(f"Your score is {self.players[0].score}")
        print(f"Computer score is {self.players[1].score}")
        if self.players[0].score > self.players[1].score:
            print(f"Congratulations! You win the Game!!")
        elif self.players[0].score < self.players[1].score:
            print(f"Computer wins the game")
    """ else:
            print(f"This round is tie! Deciding winner by coin flip...")  If we have total 5 rounds I think this codes are unnecessary"""




















