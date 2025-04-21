class Player: #5676101 (all of it)

    #Represents a player in the card game and tracks the player's hand, score, and special abilities like skip turns.
#For use when programming cpu (probably): #self.human = human  # Check whether this is a human or AI player
    def __init__(self, name: str, is_human: bool = True):

        self.name = name
        self.hand = []  # List of cards like '4 of spades'
        self.score = 0  # Player's current score
        self.skips_left = 2  # Number of turns player can skip
        self.used_special = False  # Flag if player used a special card
        self.last_special = None  # The last special card played

    def play_card(self, card: str) -> str:
        
        #Play a card from the player's hand and raises ValueError
        
        if card in self.hand:
            self.hand.remove(card)
            return card
        else:
            raise ValueError(f"{card} not in hand")

    def auto_play(self):

        #Automatically play the first card in hand (used by AI). returns played card or none if card is empty

        if self.hand:
         return self.play_card(self.hand[0])
        else:
         return None
    def skip_turn(self):

        #Skip the current turn if skips are available. Will return trues if successfully skipped , false otherwise.

        if self.skips_left > 0:
            self.skips_left -= 1
            return True
        return False

    def add_score(self, value):

        #Add points to the player's score.

        self.score += value

    def has_card(self, card):

        #Check if the player has a specific card in hand. Returns true if the card is in hand

        return card in self.hand

    def get_rank(self, card):
        
        #Extract the rank from a card string. Example: From '10 of clubs' -> '10'

        return card[:-1]  
