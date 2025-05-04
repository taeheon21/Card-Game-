from game_logic.deck import Deck
from game_logic.Player import Player
import random # (for coin flip) / I(5662884) wrote all of the codes except def __init part(5667929 wrote that part)

#5676101, I've just completely rewritten most of the code to fix some issues and maintain clarity
class Game:
    """manages the overall game flow and logic"""

    def __init__(self):  # 5667929 wrote def __init part except self.round
        """initialize the game with a deck, two players, and a set number of rounds"""
        self.deck = Deck()
        self.players = [Player("You"), Player("Computer")]  # 5676101
        self.round = 0  # 5662884
        self.total_rounds = 15  # this is new but it might make the game quicker to play (we dont need it)
        self.user_round_sum = 0
        self.computer_round_sum = 0
        self.current_figure = None
        self.deal_cards()

    def start_game(self):
        """starts the game"""
        print("Game is starting...")
        while not self.game_over():
            self.round += 1
            print(f"Round {self.round}")
            self.play_round()
        self.declare_winner()

    def deal_cards(self):  # 5676101 (Number cards are distributed 2 of each rank to the players with random suits)
        # Clear players' hands
        for player in self.players:
            player.hand = []
            # Iterate throught each rank, then through suits, so that number cards (e.g.: 2C, 2H, 3D, 3S,...) are created for both players
        for rank in self.deck.ranks:
                num_cards = []
                for suit in ['H', 'D', 'S', 'C']:
                    num_cards.append(rank + suit)
                # Shuffle for randomness of suit
                random.shuffle(num_cards)
                # In each for loop 4 cards of the same rank with all suits are created, so only 2 of those (taken from beginning) are appended to player's hand
                self.players[0].hand.extend(num_cards[:2])
                # Computer gets the remaining 2 cards
                self.players[1].hand.extend(num_cards[2:])

        for player in self.players:
            # Lambda function was used for sorting
            # Sorting is done by number(rank) (left to right, 2 to 10)
            player.hand.sort(key=lambda card: int(player.get_rank(card)))

        print("Cards have been dealt; Let the game start!")

    def play_round(self): #5676101 (90%)
        """play round, both player and computer will draw card and card values will be compared"""
        self.user_round_sum = 0
        self.computer_round_sum = 0
        user = self.players[0]  # 5676101
        computer = self.players[1]
        
        # The figure cards being drawn 5676101
        figure_card = self.deck.draw_figure_card()
        if not figure_card:
            print("All figure cards have been exhausted!")
            return
        self.current_figure = figure_card  # 5676101
        figure_id = self.current_figure[0]  # 5676101
        figure_value = self.current_figure[1]  # 5676101
        print(f"Figure card on the table: {figure_id} (worth {figure_value} points)")
        # Check if players have cards (in case they run out) (5671601)
        if not self.players[0].hand or not self.players[1].hand:
            print("Redistributing cards as one or both players have no cards left!")
            number_cards = self.deck.redistribute_number_cards()
            self.deal_cards()

        computer_card = computer.hand.pop(0)
        user_card = self.get_user_card()
        if user_card is None:
            return
        rank_user = user.get_rank(user_card)
        rank_computer = computer.get_rank(computer_card)
        # Display user's hand (5676101)
        print("Your hand:", ", ".join(self.players[0].hand))
        # Playing a card by user and computer
        print(f"You played: {user_card}")
        print(f"Computer played: {computer_card}")
        # Enforcing the 2 of Spades and 9 of Spades rule (5676101)
        if user_card == '2S' or user_card == '9S':
            user.used_special = True
            user.last_special = user_card
        else:
            user.used_special = False

        user_special = user_card == '2S' or user_card == '9S'
        computer_special = computer_card == '2S' or computer_card == '9S'

        if user_special == True and computer_special == True:
            if user_card == '9S' and computer_card != '9S':
                print("You win this round by playing special card 9 of Spades!")
                self.players[0].add_score(figure_value)
            elif computer_card == '9S' and user_card != '9S':
                print("Computer wins this round by playing 9 of Spades!")
                self.players[1].add_score(figure_value)

        # Special rule: no 3 or 10 right after using 2ofSp or 9ofSp 5676101
        if user.used_special == True and rank_user in ['3', '10']:
            raise ValueError("Error: You can't play a 3 or 10 right after using a special card like 2 of spades or 9 of spades")
        if user.used_special == True and ['3', '10'] not in user.hand:
            computer.add_score(figure_value)
            print("You don't have 3s or 10s after using special cards, therefore you skipped this round and computer wins!")
        if computer.used_special == True and rank_computer in ['3', '10']:
            raise ValueError("Error: You can't play a 3 or 10 right after using a special card like 2 of spades or 9 of spades")
        if computer.used_special == True and ['3', '10'] not in computer.hand:
            user.add_score(figure_value)
            print("Computer skipped, you win this round!")
        # For each round the sum of the values of the number cards played will be stored (5676101)
        value_user = int(rank_user)
        self.user_round_sum += value_user
        if self.user_round_sum in [12, 19]:  # If statement used to check if sum is 12 or 19 for player
            raise ValueError("Error: The sum of your played cards cannot be 12 or 19")
        value_computer = int(rank_computer)
        self.computer_round_sum += value_computer
        if self.computer_round_sum in [12, 19]:
            raise ValueError("I think a statement isn't needed here")
        for player in self.players:  # Sum of 91 exception (5676101)
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

    def get_user_card(self):  # 5676101
        prompt_range = len(self.players[0].hand) - 1
        user_input = input(f"Choose a card to play (0-{prompt_range}) or -1 to skip: ")
        card_index = int(user_input)
        # skipping mechanic
        if card_index == -1:
            if self.players[0].skip_turn():  # Checks if player can skip
                # User skips, so figure card goes to computer
                figure_id, figure_value = self.current_figure
                print(f"You skipped. Computer gets the figure card {figure_id} worth {figure_value} points.")
                self.players[1].add_score(figure_value)
                return None
            else:
                print("You can't skip more than 2 times in a game!")

        user_card = self.players[0].play_card(card_index)

        return user_card


    def get_computer_card(self):  # 5676101

        return computer_card


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




















