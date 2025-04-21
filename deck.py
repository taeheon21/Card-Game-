import random
from collections import deque
FIGURE_VALUES = {
    'A': 10, 'K': 9, 'Q': 8, 'J': 7,  # Base values for figures
    'AD': 15, 'KC': 13, 'QH': 11, 'QD': 11, 'JH': 16  # Special combinations
}

class Deck:
    """a card deck for the Get 'Em game containing numbers 2-10 (four copies each)."""

    def __init__(self):
        """start a shuffling the deck to include four instances of each number 2 through 10."""
        self.cards = []
        for number in range(2, 11):  #generate numbers 2-10
            for suit in ['hearts', 'spades', 'clubs', 'diamonds']:
                self.cards.append((number, suit))
        random.shuffle(self.cards)  #randomize card order
        #suits 
        self.suits = ['spades', 'clubs' , 'hearts' , 'diamonds'] #5662884
        #Figure cards (Ace, King, Queen, Jack)
        self.figures = ['A', 'K', 'Q', 'J'] #5662884

    def draw_card(self):
        """remove and return the top card from the deck. returns none when empty."""
        return self.cards.pop() if self.cards else None

    def is_empty(self):
        """check whether the deck has been depleted of cards."""
        return not bool(self.cards)
    def create_figure_cards(self): #5676101

        '''Create figure cards (A, K, Q, J) with their corresponding point values(figure+suit)
         We do this so that we have a double-ended queue of figure cards as tuples (id, value)
        '''
        cards = []
        # For each figure (A,K,Q,J), create cards with all four suits
        for figure in self.figures:
            for suit in self.suits:
                # Create a key for special combinations (for example: 'AD' for Ace of Diamonds)
                key = figure + suit[-1]

                # Get special value if exists, otherwise use the base figure value
                value = FIGURE_VALUES.get(key, FIGURE_VALUES[figure])

                # Store as tuple: ('KH', 9) - King of Hearts with value 9
                cards.append((key, value))

        # Shuffle the figure cards
        random.shuffle(cards)

        # Return as a deque for efficient popping from front
        return deque(cards)
   def create_number_cards(self): #5676101
        """
        Generates number cards from 2 to 10 for all suits.
           It creates a list of number cards and their suits (10 of diamonds, 2 of hearts...)
        """
        number_cards = []  # For holding number cards

        # Assuming self.ranks only has '2' to '10' 
        for val in self.ranks:
            for suit in self.suits:
                # Creation of cards (suit + rank(val))
                card = val + suit
                number_cards.append(card)
        
        random.shuffle(number_cards)

        return number_cards
