class Player: #5676101 (all of it, except def get_rank)
     '''(5676101) I created this entire function besides def get_rank; Techniques used: Basic if/else conditionals;
       data structure: list
    '''
    #Represents a player in the card game and tracks the player's hand, score, and special abilities like skip turns.

    def __init__(self, name):

        self.name = name
        self.hand = []  # List of cards like '4 of spades'
        self.score = 0  # Player's current score
        self.skips_left = 2  # Number of turns player can skip
        self.used_special = False  # Flag if player used a special card
        self.last_special = None  # The last special card played

    def play_card(self, card: str) -> str:
        
        #Play a card from the player's hand
        
        if card in self.hand:
            self.hand.remove(card)
            return card

    def skip_turn(self) -> bool:

        #Skip the current turn if skips are available. Will return trues if successfully skipped , false otherwise.

        if self.skips_left > 0:
            self.skips_left -= 1
            print(f"{self.name} skips this turn.")
            return True
        return False

    def add_score(self, value: int) -> int:

        #Add points to the player's score.

        self.score += value
        print(f"{self.name} gained {value} points!")
        return value

    def get_num(self, card: str) -> str:
        
        '''
        Extract the number as a string from a card string. Example: From '10 of clubs' -> '10' .
        It is later converted into an integer for comaprison in class Game.
        '''

        return card[:-1]  

    def get_rank(self, card): # 5662884 (I add these codes to run train_AI.py)
        rank_str = card[:-1]  # 10H' -> '10', '2S' -> '2'
        return int(rank_str)  # change into interger

  
