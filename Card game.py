import random

class Game:
    def __init__(self):
        

    def check_winner(self):
        # Automatic win (Player's score >= 91)
        for player in self.players:
            if player.score >= 91:
                print(f"{player.name} wins")
        # If there is no card anymore, decide by comparing scores or by flip a coin
        if all(len(player.hand)) == 0 for player in self.players:

            if self.players[1].score > self.players[2].score:
                print(f"{player.1} wins")

            elif self.players[1].score < self.players[2].score:
                print(f"{player.2} wins")
            #flip coin(else) I just use random I could make flip coin to decide winner.
            else:
                chosen = random.choice(self.players)
                print(f"{chosen.name} wins by a coin flip")


        # If there is no winner yet
        return None







