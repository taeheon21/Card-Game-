import random
from collections import deque
FIGURE_VALUES = {
    'A': 10, 'K': 9, 'Q': 8, 'J': 7,  # Base values for figures
    'AD': 15, 'KC': 13, 'QH': 11, 'QD': 11, 'JH': 16  # Special combinations
}

class Deck:
    # A card deck for the Get 'Em game containing numbers 2-10 (four copies each)

    def __init__(self):
        self.suits = ['spades', 'clubs' , 'hearts' , 'diamonds'] #5662884
        #Figure cards (Ace, King, Queen, Jack)
        self.figures = ['A', 'K', 'Q', 'J'] #5662884
        self.nums = ['2', '3', '4', '5', '6', '7', '8', '9', '10'] #5676101
        self.number_cards = self.create_number_cards()
        self.figure_cards = self.create_figure_cards()

    def my_shuffle(self, cards_to_shuffle): #5667929
        # my own shuffling algorithm that works pretty well (its just  Fisher-Yates shuffle)
        total_items = len(cards_to_shuffle)
    
        # going backwards through the list
        idx = total_items
        while idx > 1:
            idx -= 1
        
            # pick a random position to swap with
            pos = random.randint(0, idx)
        
        # so it dosent swapping with itself
            if pos != idx:
                #the swap
                cards_to_shuffle[idx], cards_to_shuffle[pos] = cards_to_shuffle[pos], cards_to_shuffle[idx]
    
  
        return cards_to_shuffle #5667929


    def create_figure_cards(self): #5676101

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
        cards = self.my_shuffle(cards)

        # Return as a deque for efficient popping from front
        return deque(cards)
    def create_number_cards(self): #5676101
        """
        Generates number cards from 2 to 10 for all suits.
           It creates a list of number cards and their suits (10 of diamonds, 2 of hearts...)
        """
        number_cards = []  # For holding number cards

        for val in self.nums:
            for suit in self.suits:
                # Creation of cards (suit + num(val))
                card = val + suit[0].upper()
                number_cards.append(card)
        
        return self.my_shuffle(number_cards)

        return number_cards
        
    def is_empty(self): #Check if figure card deck is empty (5676101)
        return len(self.figure_cards) == 0
        
    def draw_figure_card(self): #Used for drawing figure cards (5676101)
        if len(self.figure_cards) > 0:
            return self.figure_cards.popleft()
        else:
            return None
            
    def redistribute_number_cards(self):
        #Redistribute number cards if they run out (5676101)
        print("Redistributing number cards...")
        self.number_cards = self.create_number_cards()
        return self.number_cards
