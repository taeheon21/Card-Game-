def displayWelcomeScreen():
    """This shows the welcome stuff when game starts"""
    # added extra stars cuz it looks nicer
    print("\n****** Get 'Em Card Game ******")
    print("You vs Computer - good luck!")  # my custom welcome
    print("Highest card wins each round - simple!")


def print_round_outcome(p_card, cpu_card, who_won):
    """Shows what happened in this round"""
    #  adding extra space here cuz y not
    print(f"\nYou played: {p_card}")
    print(f"CPU played: {cpu_card}")
    # using arrow symbol looks cool
    print(f"--> {who_won} won this round")


def scoreDisplay(plyr, comp):
    """updates the scores for both players"""
    # using double-dash as separator
    print(f"\nSCORES -- You: {plyr.score} | PC: {comp.score}")
    # could add more info here later maybe


def announce_winner(champion):
    """tells everyone who won at the end"""
    # trophy emoji makes it more apiling
    print(f"\n🏆 WINNER: {champion}!! 🏆")
    # extra line just because
    print("Thanks for playing!\n")
