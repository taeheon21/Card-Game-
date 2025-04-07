import random

class Deck:
    """a card deck for the Get 'Em game containing numbers 2-10 (four copies each)."""

    def __init__(self):
        """start a shuffling the deck to include four instances of each number 2 through 10."""
        self.cards = []
        for number in range(2, 11):  #generate numbers 2-10
            self.cards += [number] * 4  #add four copies of each number
        random.shuffle(self.cards)  #randomize card order

    def draw_card(self):
        """remove and return the top card from the deck. returns none when empty."""
        return self.cards.pop() if self.cards else None

    def is_empty(self):
        """check whether the deck has been depleted of cards."""
        return not bool(self.cards)
