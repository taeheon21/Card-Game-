#I restored game.py so there are my original codes now. Here is the game.py code that Alex modified without permission
import random
from collections import deque

FIGURE_VALUES = {
    'A': 10, 'K': 9, 'Q': 8, 'J': 7,  # Base values for figures
    'AD': 15, 'KC': 13, 'QH': 11, 'QD': 11, 'JH': 16  # Special combinations
}


class Deck:
    """a card deck for the Get 'Em game containing numbers 2-10 (four copies each)."""

    def __init__(self):
        # suits
        self.suits = ['spades', 'clubs', 'hearts', 'diamonds']  # 5662884
        # Figure cards (Ace, King, Queen, Jack)
        self.figures = ['A', 'K', 'Q', 'J']  # 5662884
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10']  # 5676101
        self.number_cards = self.create_number_cards()
        self.figure_cards = self.create_figure_cards()

    def create_figure_cards(self):  # 5676101

        '''Create figure cards (A, K, Q, J) with their corresponding point values(figure+suit)
         We do this so that we have a double-ended queue of figure cards as tuples (id, value)
        '''
        cards = []
        # For each figure (A,K,Q,J), create cards with all four suits
        for figure in self.figures:
            for suit in self.suits:
                # Create a key for special combinations (for example: 'AD' for Ace of Diamonds)
                key = figure + suit[0].upper()

                # Get special value if exists, otherwise use the base figure value
                value = FIGURE_VALUES.get(key, FIGURE_VALUES[figure])

                # Store as tuple: ('KH', 9) - King of Hearts with value 9
                cards.append((key, value))

        # Shuffle the figure cards
        random.shuffle(cards)

        # Return as a deque for efficient popping from front
        return deque(cards)

    def create_number_cards(self):  # 5676101
        """
        Generates number cards from 2 to 10 for all suits.
           It creates a list of number cards and their suits (10 of diamonds, 2 of hearts...)
        """
        number_cards = []  # For holding number cards

        # Assuming self.ranks only has '2' to '10'
        for val in self.ranks:
            for suit in self.suits:
                # Creation of cards (suit + rank(val))
                card = val + suit[0].upper()
                number_cards.append(card)

        random.shuffle(number_cards)

        return number_cards

    def is_empty(self):  # Check if figure card deck is empty (5676101)
        return len(self.figure_cards) == 0

    def draw_figure_card(self):  # Used for drawing figure cards (5676101)
        if len(self.figure_cards) > 0:
            return self.figure_cards.popleft()
        else:
            return None

    def redistribute_number_cards(self):
        # Redistribute number cards if they run out (5676101)
        print("Redistributing number cards...")
        self.number_cards = self.create_number_cards()
        return self.number_cards


class Player:  # 5676101 (all of it)

    # Represents a player in the card game and tracks the player's hand, score, and special abilities like skip turns.
    def __init__(self, name):

        self.name = name
        self.hand = []  # List of cards like '4S (4 of spades)'
        self.score = 0  # Player's current score
        self.skips_left = 2  # Number of turns player can skip
        self.used_special = False  # Flag if player used a special card
        self.last_special = None  # The last special card played

    def play_card(self, card):

        # Play a card from the player's hand and raises ValueError

        if card in self.hand:
            self.hand.remove(card)
            return card

    def auto_play(self):

        # Automatically play the first card in hand (used by AI). returns played card or none if card is empty

        if self.hand:
            return self.play_card(self.hand[0])
        else:
            return None

    def skip_turn(self):

        # Skip the current turn if skips are available. Will return trues if successfully skipped , false otherwise.

        if self.skips_left > 0:
            self.skips_left -= 1
            print(f"{self.name} skips this turn.")
            return True
        return False

    def add_score(self, value):

        # Add points to the player's score.

        self.score += value
        print(f"{self.name} gained {value} points!")
        return value

    def has_card(self, card):

        # Check if the player has a specific card in hand. Returns true if the card is in hand

        return card in self.hand

    def get_rank(self, card):

        # Extract the rank from a card string. Example: From '10 of clubs' -> '10'

        return card[:-1]


class Game:
    # Manages the overall game flow and logic

    def __init__(self):
        # Initialize the game with a deck, two players, and a set number of rounds
        self.deck = Deck()
        self.players = [Player("You"), Player("Computer")]
        self.round = 0
        self.total_rounds = 15
        self.user_round_sum = 0
        self.computer_round_sum = 0
        self.current_figure = None
        self.deal_cards()

    def start_game(self): #Taeheon
        #Starts the game
        print("Game is starting...")
        while not self.game_over():
            self.round += 1
            print(f"Round {self.round}")
            self.play_round()
        self.declare_winner()

    def deal_cards(self):
        # Clear players' hands
        for player in self.players:
            player.hand = []

        # Distribute cards - 2 of each rank to each player with random suits
        for rank in self.deck.ranks:
                num_cards = []
                for suit in ['H', 'D', 'S', 'C']:
                    num_cards.append(rank + suit)
                # Shuffle for randomness of suit
                random.shuffle(num_cards)

                # Player 1 gets the first 2 cards
                self.players[0].hand.extend(num_cards[:2])
                # Player 2 gets the remaining 2 cards
                self.players[1].hand.extend(num_cards[2:])

        for player in self.players:
            # Sort cards by rank
            player.hand.sort(key=lambda card: int(player.get_rank(card)))

        print("Cards have been dealt; Let the game start!")

    def play_round(self):
        # Play round, both player and computer will draw card and card values will be compared
        self.user_round_sum = 0
        self.computer_round_sum = 0
        user = self.players[0]
        computer = self.players[1]

        #Display players' scores
        print(f"Your score: {self.players[0].score}")
        print(f"Computer score: {self.players[1].score}")

        # Check if players are restricted from playing 3s and 10s
        if user.used_special:
            # So, after using a special card, 3s and 10s will be checked
            has_three_or_ten = False
            for card in user.hand:
                if card.startswith('3') or card.startswith('10'):
                    has_three_or_ten = True
                    break  # No need to check further if we found one

            if not has_three_or_ten:
                print("You don't have 3s or 10s after using special cards, therefore you skip this round!")

                # Important: we need to reset the special card usage bool value
                player.used_special = False

                # Computer gets card
                drawn_card = self.deck.draw_figure_card()
                if drawn_card is not None:
                    fig_card_id, fig_card_value = drawn_card
                    computer.add_score(fig_card_value)
                    print(f"Computer gets the figure card {fig_card_id} worth {fig_card_value} points.")

                return  # Player skips their turn here

        if computer.used_special:
            # The same rule applies to computer
            comp_has_three_or_ten = False
            for c in computer.hand:
                if c.startswith('3') or c.startswith('10'):
                    comp_has_three_or_ten = True
                    break

            if not comp_has_three_or_ten:
                print("Computer doesn't have 3s or 10s after using special cards, therefore computer skips this round!")

                # Resetting the bool value so it doesn't affect the next turn
                computer.used_special = False

                # Player gets card
                drawn_figure = self.deck.draw_figure_card()
                if drawn_figure is not None:  # Check for empty draws (unlikely event)
                    figure_id, figure_value = drawn_card
                    user.add_score(figure_value)
                    print(f"You get the figure card {figure_id} worth {figure_value} points.")

                return

        # Draw figure card
        figure_card = self.deck.draw_figure_card()
        if not figure_card:
            print("All figure cards have been exhausted!")
            return
        self.current_figure = figure_card
        figure_id = self.current_figure[0]
        figure_value = self.current_figure[1]
        print(f"Figure card on the table: {figure_id} (worth {figure_value} points)")

        # Check if players have cards (in case they run out)
        if not self.players[0].hand or not self.players[1].hand:
            print("Redistributing cards as one or both players have no cards left!")
            number_cards = self.deck.redistribute_number_cards()
            self.deal_cards()

        # Display user's hand
        print("Your hand:", ", ".join(self.players[0].hand))

        # Get cards from players
        user_card = self.get_user_card()
        if user_card is None:  # User skipped (part of error fixing)
            return

        computer_card = computer.hand.pop(0)

        # Display cards played
        print(f"You played: {user_card}")
        print(f"Computer played: {computer_card}")

        # Special cards logic (2 of Spades and 9 of Spades)
        user_special = user_card == '2S' or user_card == '9S'
        computer_special = computer_card == '2S' or computer_card == '9S'

        # If any player played a special card
        if user_special or computer_special:
            if user_special and computer_special:
                # Both played special cards - 9S has priority
                if user_card == '9S' and computer_card != '9S':
                    print("You win this round by playing special card 9 of Spades!")
                    user.add_score(figure_value)
                elif computer_card == '9S' and user_card != '9S':
                    print("Computer wins this round by playing 9 of Spades!")
                    computer.add_score(figure_value)
            elif user_special:
                # Only user played special card
                print(f"You win this round by playing special card {user_card}!")
                user.add_score(figure_value)
            else:
                # Only computer played special card
                print(f"Computer wins this round by playing special card {computer_card}!")
                computer.add_score(figure_value)

            # Track who used special cards (for next round restrictions)
            if user_special:
                user.used_special = True
                user.last_special = user_card
            else:
                user.used_special = False

            if computer_special:
                computer.used_special = True
                computer.last_special = computer_card
            else:
                computer.used_special = False

            return

        # Reset special card boolean values if neither player used special cards
        user.used_special = False
        computer.used_special = False

        # Get ranks for comparison
        rank_user = user.get_rank(user_card)
        rank_computer = computer.get_rank(computer_card)

        # Get number value for player cards
        value_user = int(user.get_rank(user_card))
        value_computer = int(computer.get_rank(computer_card))

        # 12 19 Rule enforced
        self.user_round_sum += value_user
        if self.user_round_sum in [12, 19]:
            print(f"Warning: The sum of your played cards is {self.user_round_sum}, which is not allowed!")
            print("You automatically lose this round!")
            computer.add_score(figure_value)
            return

        self.computer_round_sum += value_computer
        if self.computer_round_sum in [12, 19]:
            print(f"Warning: The sum of your played cards is {self.computer_round_sum}, which is not allowed!")
            print("You automatically lose this round!")
            user.add_score(figure_value)
            return

        # Check for score of 101
        for player in self.players:
            if player.score >= 101:
                print(f"{player.name} wins with 91 points!")

        # Compare number cards (Taeheon)
        if value_user > value_computer:
            print("You win this round!")
            user.add_score(figure_value)
        elif value_user < value_computer:
            print("Computer wins this round!")
            computer.add_score(figure_value)
        else:
            print(f"This round is a tie! Play another card to break the tie...")
            self.handle_tie()

    def handle_tie(self):
        # Handle tie situation: Players play again, if tied again, coin flip decides
        user = self.players[0]
        computer = self.players[1]
        figure_value = self.current_figure[1]

        # Check if both players have cards left for tiebreaker
        if not user.hand or not computer.hand:
            print("Not enough cards for tiebreaker! Deciding by coin flip...")
            winner = random.choice([user, computer]) #Taeheon
            winner.add_score(figure_value)
            print(f"{winner.name} wins by coin flip!")
            return

        print("Your hand:", ", ".join(user.hand))

        # Get tiebreaker cards
        user_card = self.get_user_card()
        if user_card is None:  # User skipped (shouldn't happen in tiebreaker)
            return

        computer_card = computer.hand.pop(0)

        print(f"Tiebreaker - You played: {user_card}")
        print(f"Tiebreaker - Computer played: {computer_card}")

        # Check for special cards first
        user_special = user_card == '2S' or user_card == '9S'
        computer_special = computer_card == '2S' or computer_card == '9S'

        if user_special or computer_special:
            if user_special and computer_special:
                # Both played special cards - 9S has priority
                if user_card == '9S' and computer_card != '9S':
                    print("You win the tiebreaker by playing special card 9 of Spades!")
                    user.add_score(figure_value)
                elif computer_card == '9S' and user_card != '9S':
                    print("Computer wins the tiebreaker by playing special card 9 of Spades!")
                    computer.add_score(figure_value)
            elif user_special:
                # Only user played special card
                print(f"You win the tiebreaker by playing special card {user_card}!")
                user.add_score(figure_value)
            else:
                # Only computer played special card
                print(f"Computer wins the tiebreaker by playing special card {computer_card}!")
                computer.add_score(figure_value)
            return  # End tiebreaker after special card

        # Get values for comparison and check sum restrictions
        value_user = int(user.get_rank(user_card))
        value_computer = int(computer.get_rank(computer_card))

        self.user_round_sum += value_user
        if self.user_round_sum in [12, 19]:
            print(f"Warning: The sum of your played cards is {self.user_round_sum}, which is not allowed!")
            print("You automatically lose this round!")
            computer.add_score(figure_value)
            return

        self.computer_round_sum += value_computer
        if self.computer_round_sum in [12, 19]:
            print(f"Warning: The sum of your played cards is {self.computer_round_sum}, which is not allowed!")
            print("You automatically lose this round!")
            user.add_score(figure_value)
            return

        # Compare tiebreaker cards
        if value_user > value_computer:
            print("You win the tiebreaker!")
            user.add_score(figure_value)
        elif value_user < value_computer:
            print("Computer wins the tiebreaker!")
            computer.add_score(figure_value)
        else:
            print("Tiebreaker is also a tie! Deciding by coin flip...")
            winner = random.choice([user, computer])
            winner.add_score(figure_value)
            print(f"{winner.name} wins by coin flip!")

    def get_user_card(self):
        user = self.players[0]
        prompt_range = len(user.hand) - 1
    # Although not essential to the logic, used while, try for better error handling
        while True:
            try:
                user_input = input(f"Choose a card to play (0-{prompt_range}) or -1 to skip: ")
                card_index = int(user_input)

                # Validate input range
                if card_index != -1 and (card_index < 0 or card_index > prompt_range):
                    print(f"Invalid input! Please enter a number between 0 and {prompt_range}")
                    continue

                # Handle skipping
                if card_index == -1:
                    if user.skip_turn():  # Checks if player can skip
                        user.used_special = False
                        # User skips, so figure card goes to computer
                        figure_id, figure_value = self.current_figure
                        print(f"You skipped. Computer gets the figure card {figure_id} worth {figure_value} points.")
                        self.players[1].add_score(figure_value)
                        return None
                    else:
                        print("You can't skip more than 2 times in a game!")
                        continue

                # Get the chosen card
                chosen_card = user.hand[card_index]

                # Check if the card can be played (3 or 10 restriction)
                if user.used_special and (chosen_card.startswith('3') or chosen_card.startswith('10')):
                    print("Error: You can't play a 3 or 10 right after using a special card!")
                    print("You must play a different card.")
                    continue

                # Play the card
                user_card = user.play_card(chosen_card)
                return user_card

            except ValueError:
                print("Invalid input! Please enter a valid number.")
                continue
            except IndexError:
                print(f"Invalid card selection! Please enter a number between 0 and {prompt_range}")
                continue

    def game_over(self): #Taeheon
        #Check if game completion conditions are satisfied(round expired or deck is empty)
        for player in self.players:
            if player.score >= 101:
                return True

        return self.round >= self.total_rounds or self.deck.is_empty()

    def declare_winner(self): #Taeheon
        #Declare final winner
        print("Game Over!")
        print(f"Your score is {self.players[0].score}")
        print(f"Computer score is {self.players[1].score}")
        if self.players[0].score > self.players[1].score:
            print(f"Congratulations! You win the Game!!")
        elif self.players[0].score < self.players[1].score:
            print(f"Computer wins the game")
        else:
            print(f"The game is a tie!")

if __name__ == "__main__":
    game = Game()
    game.start_game()
