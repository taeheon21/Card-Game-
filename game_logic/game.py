'''from game_logic.deck import Deck
from game_logic.player import Player
import random # (for coin flip) / I(5662884) wrote all of the codes except def __init part(5667929 wrote that part)


class Game:
    """manages the overall game flow and logic"""

    def __init__(self):  # 5667929 wrote def __init part except self.round
        """initialize the game with a deck, two players, and a set number of rounds"""
        self.deck = Deck()
        self.player = Player("you")
        self.computer = Player("computer")
        self.round = 0  # 5662884
        self.total_rounds = 5  # this is new but it might make the game quicker to play (we dont need it)

    def start_game(self):  #5662884
        """starts the game"""
        print("Game is starting...")
        while not self.game_over():
            self.round += 1
            print(f"Round {self.round}")
            self.play_round()
        self.declare_winner()


    def play_round(self): #5662884
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
            print(f"This round is a tie! Deciding winner by coin flip...")
            winner = random.choice([self.player, self.computer])
            if winner is self.player:
                print(f"You win {self.round} by coin flip!")
                self.player.add_score(card_player)
            else:
                print(f"Computer wins {self.round} by coin flip!")
                self.computer.add_score(card_computer)


    def game_over(self): #5662884
        """check if game completion conditions are satisfied(round expired or deck is empty)"""
        return self.round >= self.total_rounds or self.deck.is_empty()


    def declare_winner(self): #5662884
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
                user.used_special = False

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
        if not figure_card: #Taeheon
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
        def special_card(card):
            return card in ('2S', '9S')

        user_special = special_card(user_card)

        computer_special = special_card(computer_card)

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
        num_user = user.get_num(user_card)
        num_computer = computer.get_num(computer_card)

        # Get number value for player cards
        value_user = int(user.get_num(user_card))
        value_computer = int(computer.get_num(computer_card))

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
                print(f"{player.name} wins with 101 points!")

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

'''
import random
from .deck import Deck
from .Player import Player


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

    def start_game(self):  # Taeheon
        # Starts the game
        print("Game is starting...")
        while not self.game_over():
            self.round += 1
            print(f"Round {self.round}")
            self.play_round()
        self.declare_winner()

    def deal_cards(self): #5676101
        # Clear players' hands
        for player in self.players:
            player.hand = []

        # Distribute cards - 2 of each rank to each player with random suits
        for num in self.deck.nums:
            num_cards = []
            for suit in ['H', 'D', 'S', 'C']:
                num_cards.append(num + suit)
            # Shuffle for randomness of suit
            self.deck.my_shuffle(num_cards)

            # Player 1 gets the first 2 cards
            self.players[0].hand.extend(num_cards[:2])
            # Player 2 gets the remaining 2 cards
            self.players[1].hand.extend(num_cards[2:])

        for player in self.players:
            # Sort cards by number
            player.hand.sort(key=lambda card: int(player.get_num(card)))

        print("Cards have been dealt; Let the game start!")

    # The old play_round is now commented out
    # These parameters are determined through UI class
    def play_round(self, user_card, computer_card, figure_card):
        self.user_round_sum = 0
        self.computer_round_sum = 0
        user = self.players[0]
        computer = self.players[1]

        figure_id = figure_card[0]
        figure_value = figure_card[1]
        self.current_figure = figure_card

        print(f"Your score: {self.players[0].score}")
        print(f"Computer score: {self.players[1].score}")

        # Check if players are restricted from playing 3s and 10s (5676101)
        if user.used_special:
            # So, after using a special card, 3s and 10s will be checked
            has_three_or_ten = False
            for card in user.hand:
                if card.startswith('3') or card.startswith('10'):
                    has_three_or_ten = True
                    break  # No need to check further if we found one

            if not has_three_or_ten:
                print("You don't have 3s or 10s after using special cards, therefore you skip this round!")
                user.used_special = False

                # Computer gets card
                drawn_card = self.deck.draw_figure_card()
                if drawn_card is not None:
                    fig_card_id, fig_card_value = drawn_card
                    computer.add_score(fig_card_value)
                    print(f"Computer gets the figure card {fig_card_id} worth {fig_card_value} points.")

                return f"Computer gets the figure card {fig_card_id} worth {fig_card_value} points."

        if computer.used_special:
            # The same rule applies to computer
            comp_has_three_or_ten = False
            for c in computer.hand:
                if c.startswith('3') or c.startswith('10'):
                    comp_has_three_or_ten = True
                    break

            if not comp_has_three_or_ten:
                print("Computer doesn't have 3s or 10s after using special cards, therefore computer skips this round!")
                computer.used_special = False

                # Player gets card
                drawn_figure = self.deck.draw_figure_card()
                if drawn_figure is not None:  # Check for empty draws (unlikely event)
                    figure_id, figure_value = drawn_figure
                    user.add_score(figure_value)
                    print(f"You get the figure card {figure_id} worth {figure_value} points.")

                return f"You get the figure card {figure_id} worth {figure_value} points."

        print(f"Figure card on the table: {figure_id} (worth {figure_value} points)")
        print(f"You played: {user_card}")
        print(f"Computer played: {computer_card}")

        # Redistribute if hands are empty
        if not user.hand or not computer.hand:
            print("Redistributing cards as one or both players have no cards left!")
            self.deck.redistribute_number_cards()
            self.deal_cards()
            
        # Special cards logic (2 of Spades and 9 of Spades) (5676101)
        # This function returns either True or False if card is 2S or 9S
        def special_card(card):
            return card in ('2S', '9S')

        user_special = special_card(user_card)
        computer_special = special_card(computer_card)
        # If any played special (5676101)
        if user_special or computer_special:
            # If both played special
            if user_special and computer_special:
                if user_card == '9S' and computer_card != '9S':
                    print("You win this round by playing special card 9 of Spades!")
                    user.add_score(figure_value)
                    # Special card tracking modified (5676101)
                    user.used_special = True
                    user.last_special = user_card
                    computer.used_special = True
                    computer.last_special = computer_card
                    return "You win with 9S!"
                elif computer_card == '9S' and user_card != '9S':
                    print("Computer wins this round by playing 9 of Spades!")
                    computer.add_score(figure_value)
                    # Same here
                    user.used_special = True
                    user.last_special = user_card
                    computer.used_special = True
                    computer.last_special = computer_card
                    return "Computer wins with 9S!"
                else:
                    print("Both played special cards. 9S has priority.")

            elif user_special:
                print(f"You win this round by playing special card {user_card}!")
                user.add_score(figure_value)
                user.used_special = True
                user.last_special = user_card
                return f"You win with special card {user_card}!"
            else:
                print(f"Computer wins this round by playing special card {computer_card}!")
                computer.add_score(figure_value)
                computer.used_special = True
                computer.last_special = computer_card
                return f"Computer wins with special card {computer_card}!"

            '''Original tracking worked the following way
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
            
             return "Special card resolution."'''

        # Reset bool values if no specials used
        user.used_special = False
        computer.used_special = False

        value_user = int(user.get_num(user_card))
        value_computer = int(computer.get_num(computer_card))

        self.user_round_sum += value_user
        if self.user_round_sum in [12, 19]:
            print(f"Warning: The sum of your played cards is {self.user_round_sum}, which is not allowed!")
            print("You automatically lose this round!")
            computer.add_score(figure_value)
            return "Sum of you played cards is 12 or 19. You lose!"

        self.computer_round_sum += value_computer
        if self.computer_round_sum in [12, 19]:
            print(f"Warning: The sum of computer's played cards is {self.computer_round_sum}, which is not allowed!")
            print("Computer automatically loses this round!")
            user.add_score(figure_value)
            return "Sum of computer cards is 12 or 19. You win!"

        for player in self.players:
            if player.score >= 101:
                print(f"{player.name} wins with 101 points!")

        if value_user > value_computer:
            print("You win this round!")
            user.add_score(figure_value)
            return "You win!"
        elif value_user < value_computer:
            print("Computer wins this round!")
            computer.add_score(figure_value)
            return "Computer wins!"
        else:
            '''Initially:
            return self.handle_tie()'''
            # Changed:
            print(f"This round is a tie! Play another card to break the tie")
            return "Tie, play another card!"

    # Original tie handling
    '''def handle_tie(self):
        # Handle tie situation: Players play again, if tied again, coin flip decides
        user = self.players[0]
        computer = self.players[1]
        figure_value = self.current_figure[1]
        winner = random.choice([user, computer])  # Taeheon
        winner.score += figure_value 

        return f"{winner.name} wins by coin flip! +{figure_value}" # taeheon


        # Check if both players have cards left for tiebreaker
        if not user.hand or not computer.hand:
            print("Not enough cards for tiebreaker! Deciding by coin flip...")
            winner = random.choice([user, computer])  # Taeheon
            winner.add_score(figure_value)
            print(f"{winner.name} wins by coin flip!")
            return

        print("Your hand:", ", ".join(user.hand))

        # Get tiebreaker cards
        user_card = self.get_user_card()
        if user_card is None:
            return

        computer_card = computer.hand.pop(0)

        print(f"Tiebreaker - You played: {user_card}")
        print(f"Tiebreaker - Computer played: {computer_card}") 

        # Check for special cards first
        def special_card(card):
            return card in ('2S', '9S')

        user_special = special_card(user_card)

        computer_special = special_card(computer_card)

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
        value_user = int(user.get_num(user_card))
        value_computer = int(computer.get_num(computer_card))

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
            print("Tiebreaker is also a tie! Deciding by coin flip...")  # 5662884
            winner = random.choice([user, computer])
            winner.add_score(figure_value)
            print(f"{winner.name} wins by coin flip!")'''

    # A new fucntion was added as replacement (5676101)
    def handle_tie2(self, user_card, computer_card, figure_card):
        user = self.players[0]
        computer = self.players[1]
        figure_value = figure_card[1]

        print(f"Tiebreaker: You played: {user_card}")
        print(f"Tiebreaker: Computer played: {computer_card}")

        # Check if computer's card violate tiebreak sum rule (5676101)
        # We need to check against the computer's first card in tiebreak
        if hasattr(self, '_tiebreak_first_computer_card'):
            first_card_value = int(self._tiebreak_first_computer_card[:-1])  # Get number from card
            current_card_value = int(computer_card[:-1])
            computer_tiebreak_sum = first_card_value + current_card_value

            if computer_tiebreak_sum in [12, 19]:
                print(f"Computer's tiebreak sum is {computer_tiebreak_sum}! Computer forfeits.")
                user.add_score(figure_value)
                return "Computer violates sum rule - You win!"

        # Check for special cards first
        def special_card(card):
            return card in ('2S', '9S')

        user_special = special_card(user_card)
        computer_special = special_card(computer_card)

        if user_special or computer_special:
            if user_special and computer_special:
                # Both played special cards - 9S has priority
                if user_card == '9S' and computer_card != '9S':
                    print("You win the tiebreaker by playing special card 9 of Spades!")
                    user.add_score(figure_value)
                    return "You win tiebreak with 9S!"
                elif computer_card == '9S' and user_card != '9S':
                    print("Computer wins the tiebreaker by playing special card 9 of Spades!")
                    computer.add_score(figure_value)
                    return "Computer wins tiebreak with 9S!"
            
            elif user_special:
                # Only user played special card
                print(f"You win the tiebreaker by playing special card {user_card}!")
                user.add_score(figure_value)
                return f"You win tiebreak with {user_card}!"
            else:
                # Only computer played special card
                print(f"Computer wins the tiebreaker by playing special card {computer_card}!")
                computer.add_score(figure_value)
                return f"Computer wins tiebreak with {computer_card}!"

        # Get values for comparison 
        value_user = int(user.get_num(user_card))
        value_computer = int(computer.get_num(computer_card))

        # Card comparison (Taeheon)
        if value_user > value_computer:
            print("You win the tiebreaker!")
            user.add_score(figure_value)
            return "You win tiebreak!"
        elif value_user < value_computer:
            print("Computer wins the tiebreaker!")
            computer.add_score(figure_value)
            return "Computer wins tiebreak!"
        else:
            print("Tiebreaker is also a tie! Will decide by coin flip")
            return "Tie again, coin flip!"

    # Method to set computer's first tiebreak card (5676101)
    def set_first_comp_card(self, card):
        self._tiebreak_first_computer_card = card
        return True

        # Method to reset tiebreak state (5676101)
    def clear_tiebreak(self):
        if hasattr(self, '_tiebreak_first_computer_card'):
            delattr(self, '_tiebreak_first_computer_card')
            return True
        return False

    # New method for coinflip had to be added (5676101)
    def resolve_tie_coinflip(self, figure_card):
        user = self.players[0]
        computer = self.players[1]
        figure_value = figure_card[1]

        winner = random.choice([user, computer])
        winner.add_score(figure_value)
        print(f"Coin flip result: {winner.name} wins!")
        return f"{winner.name} wins by coin flip!"

    def get_user_card(self): #(5676101)
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


                '''if card_index == -1:
                    if user.skip_turn():  # Checks if player can skip
                        user.used_special = False
                        # User skips, so figure card goes to computer
                        figure_id = self.current_figure[0]
                        figure_value = self.current_figure[1]
                        print(f"You skipped. Computer gets the figure card {figure_id} worth {figure_value} points.")
                        self.players[1].add_score(figure_value)
                        return None
                    else:
                        print("You can't skip more than 2 times in a game!")
                        continue'''

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

    def skip_round(self, comp_card: str, figure: tuple): #(Taeheon)
        self.computer.play_card(comp_card)  # remove computer card from computer's hand
        pts = figure[1]  # computer gets points
        self.computer.score += pts
        return f"Computer wins (skip) +{pts}"

    def game_over(self):  # Taeheon
        # Check if game completion conditions are satisfied(round expired or deck is empty)
        for player in self.players:
            if player.score >= 101:
                return True

        return self.round >= self.total_rounds or self.deck.is_empty()

    def declare_winner(self):  # Taeheon
        # Declare final winner
        print("Game Over!")
        return "Game over"
        print(f"Your score is {self.players[0].score}")
        return f" Your score is {self.players[0].score}"
        print(f"Computer score is {self.players[1].score}")
        return f" Computer score is {self.players[1].score}"
        if self.players[0].score > self.players[1].score:
            print(f"Congratulations! You win the Game!!")
            return "Congratulations! You win the Game!!"
        elif self.players[0].score < self.players[1].score:
            print(f"Computer wins the game")
            return "Computer wins the game!"
        else:
            print(f"The game is a tie!")
            return "The game is a tie!"

"""
the first draft
from game_logic.deck import Deck
from game_logic.player import Player

class Game:
    manages the overall game flow and logic

    def __init__(self):
      initialize the game with a deck, two players, and a set number of rounds
        self.deck = Deck()
        self.player = Player("you")
        self.computer = Player("computer")
        self.rounds = 5 #this is new but it might make the game quicker to play (we dont need it)


 needs a function to start the game, another to play the round, another to check all roounds are done, and a function to check if the game is over
"""
