class Player: #5676101 (all of it)

    #Represents a player in the card game and tracks the player's hand, score, and special abilities like skip turns.
#For use when programming cpu as boolean (probably): #self.human = human  # Check whether this is a human or AI player
    def __init__(self, name):

        self.name = name
        self.hand = []  # List of cards like '4 of spades'
        self.score = 0  # Player's current score
        self.skips_left = 2  # Number of turns player can skip
        self.used_special = False  # Flag if player used a special card
        self.last_special = None  # The last special card played

    def play_card(self, card):
        
        #Play a card from the player's hand and raises ValueError
        
        if card in self.hand:
            self.hand.remove(card)
            return card

    def skip_turn(self):

        #Skip the current turn if skips are available. Will return trues if successfully skipped , false otherwise.

        if self.skips_left > 0:
            self.skips_left -= 1
            print(f"{self.name} skips this turn.")
            return True
        return False

    def add_score(self, value):

        #Add points to the player's score.

        self.score += value
        print(f"{self.name} gained {value} points!")
        return value

    def has_card(self, card):

        #Check if the player has a specific card in hand. Returns true if the card is in hand

        return card in self.hand

    def get_num(self, card):
        
        #Extract the number from a card string. Example: From '10 of clubs' -> '10'

        return card[:-1]  
