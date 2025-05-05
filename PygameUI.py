#Work To Do: handle specical rules + add skip button + add background audio
import pygame
import random
from game_logic.deck import Deck
from game_logic.Player import Player
from game_logic.game import Game

from collections import defaultdict
import sys # for quiting the game once its over

pygame.init()

def displayWelcomeScreen():
    screen.fill(green)
    font = pygame.font.SysFont(None, 40)

    welcome_message= ["\n****** Get 'Em Card Game ******",
    "You vs Computer - good luck!",
    "Highest card wins each round - simple!",
    "Press key to start"]

    for i, line in enumerate(welcome_message):
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(screen.get_width() // 2, 240 + i * 60))
        screen.blit(text, text_rect)

    pygame.display.flip()
    # Wait for user to press a key
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False 

def announce_winner(champion):
    """tells everyone who won at the end"""
    # trophy emoji makes it more apiling
    print(f"\n🏆 WINNER: {champion}!! 🏆")
    # extra line just because
    print("Thanks for playing!\n") 

#Creating a window(The playing area):
screen = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Get 'Em ")

#coloring the playing area
green = (10, 110, 10)


#cards size and colour
CARD_WIDTH = 60
CARD_HEIGHT = 90
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

#figure cards size
FIGURE_CARD_WIDTH = 70
FIGURE_CARD_HEIGHT = 105


class Card:
    def __init__(self, position_x, position_y ,value,suit=None,image_filename=None,width=CARD_WIDTH, height=CARD_HEIGHT, border_color=BLACK):
        #set the card position and size relative to the screen
        self.rect = pygame.Rect(position_x, position_y, width, height)
        
        self.value = value #stores card's value
        self.suit = suit    #tores card's suit
        self.border_color = border_color 

        #load image, if not found, create a fallback drawing (backup case)
        if image_filename is not None:
            self.image = pygame.image.load(image_filename)
            self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        else:
            self.image = None

    def draw(self, screen): 

        # Create a slightly bigger golden rectangle for figure cards
        if self.border_color == (255, 215, 0):  # GOLD
            border_rect = self.rect.inflate(4, 4).move(-4, -3) 
            pygame.draw.rect(screen, self.border_color, border_rect, 3)
        else:
        #Regular black border for Non-figure cards
            pygame.draw.rect(screen, self.border_color, self.rect, 1)

        # Draw the card image at its designated position
        if self.image:
            screen.blit(self.image, self.rect.topleft)

        else: # If the card has no image, draw a plain rectangle with the card's value and suit
            pygame.draw.rect(screen, WHITE, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 1)
            font = pygame.font.SysFont(None, 30)
            text = font.render(f"{self.value} {self.suit[0].upper()}", True, BLACK)
            # Center the text inside the rectangle
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)

def get_card_image_path(value, suit):
    value_str = str(value).lower()
    suit_str = suit.lower()
    return f"assets/cards/png/{value_str}_of_{suit_str}.png"

card_spacing = 6
total_width = (CARD_WIDTH * 9) + (card_spacing * 8)
start_x = (screen.get_width() - total_width) // 2

deck = Deck()  # Create a new shuffled deck
cards = deck.create_number_cards()
random.shuffle(cards)
grouped_cards = defaultdict(list)
for card_str in cards:
    value = card_str[:-1]  # all characters except the last
    suit_letter = card_str[-1]
    suit_lookup = {'H': 'hearts', 'D': 'diamonds', 'S': 'spades', 'C': 'clubs'}
    suit = suit_lookup[suit_letter]
    grouped_cards[value].append((value, suit))

player_cards = []
computer_cards = []
for value in range(2, 11):  # For each value from 2 to 10
    value_str = str(value)
    suits = grouped_cards[value_str]

    # First 2 go to player, last 2 go to computer
    player_cards.extend(suits[:2])
    computer_cards.extend(suits[2:])

player =Player("You")
computer = Player("Computer")

player.hand = player_cards  # Assign the list of 18 cards
computer.hand = computer_cards
player.hand = [f"{val}{suit[0].upper()}" for val, suit in player_cards]
computer.hand = [f"{val}{suit[0].upper()}" for val, suit in computer_cards]

player_hand = []
computer_hand = []

# Fill player and computer hands
for plyer, (value, suit) in enumerate(player_cards):
        
        x = start_x + (plyer  % 9) * (CARD_WIDTH + card_spacing)
        y = 500  + (plyer // 9) * (CARD_HEIGHT + 10)
        image_path = get_card_image_path(value, suit)
        player_hand.append(Card(x, y, value, suit, image_path))

for comp, (value, suit) in enumerate(computer_cards):    # Computer gets every odd-indexed card
        x = start_x + (comp % 9) * (CARD_WIDTH + card_spacing)
        y = 33 + (comp // 9) * (CARD_HEIGHT + 10)
        image_path = get_card_image_path(value, suit)
        computer_hand.append(Card(x, y, value, suit, image_path))


figure_cards = deck.create_figure_cards() # shuffled list of figure cards(imported from the deck class)
center_figure = deck.draw_figure_card()  # pick one figure card from the top


#Helper function to turn figure code like 'QD' into a usable image path
def get_figure_image_path(figure_code):

    figure_code = figure_code.upper() 

    lookup = {
        'A': 'ace', 'K': 'king', 'Q': 'queen', 'J': 'jack'
    }
    figure = lookup[figure_code[0]]
    suit = {
        'H': 'hearts', 'D': 'diamonds', 'S': 'spades', 'C': 'clubs'
    }[figure_code[1]]

    return f"assets/cards/png/{figure}_of_{suit}.png"

center_image_path = get_figure_image_path(center_figure[0]) # Get the figure card image path

#Center the figure card + Add gold border around the figure card
GOLD = (255, 215, 0)

center_figure_card = Card(
    565, 290,                          # Position
    center_figure[1],                 # Value
    suit=None,
    image_filename=center_image_path,
    width=FIGURE_CARD_WIDTH,          # Bigger size
    height=FIGURE_CARD_HEIGHT,
    border_color=GOLD                 # Gold border
)

round_in_progress = False
round_ended = False
round_end_time = 0
displayWelcomeScreen() #Welcome message!

def run_game(center_figure, figure_cards):
    game_is_running = True
    selected_card = None
    computer_card = None
    round_outcome = None
    warning = ""
    warning_timer = 0

    show_result_until = None
    round_phase = "waiting_for_play"
    phase_timer = None

    played_player_card = None
    played_computer_card = None

    game = Game()
    game.player = player
    game.computer = computer

    while game_is_running:
        screen.fill(green)

        if warning and pygame.time.get_ticks() > warning_timer:
            warning = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_running = False

            if round_phase == "waiting_for_play" and event.type == pygame.MOUSEBUTTONDOWN and not selected_card:
                mouse_pos = pygame.mouse.get_pos()
                
                for card in player_hand:
                    if card.rect.collidepoint(mouse_pos):
                        selected_card = card
                        selected_card_str = f"{card.value}{card.suit[0].upper()}"
                        selected_card.rect.topleft = (screen.get_width() // 2 + 100, screen.get_height() // 2)
                        break

                if selected_card:
                    if selected_card_str not in player.hand:
                        warning = "Card not in hand!"
                        warning_timer = pygame.time.get_ticks() + 3000
                        selected_card = None
                        continue
                    # Special card logic (optional)
                    if selected_card_str in ['2S', '9S']:
                        player.used_special = True
                        player.last_special = selected_card_str
                    else:
                        if player.last_special in ["2S", "9S"] and selected_card.value in ["3", "9"]:
                            warning = "You can't play 3 or 10 after 2S or 9S!"
                            warning_timer = pygame.time.get_ticks() + 3000
                            selected_card = None
                            continue
                        
                     # Remove from both hands
                    selected_card.rect.topleft = (screen.get_width() // 2 + 100, screen.get_height() // 2)
                    played_player_card = selected_card  # Save it for drawing
                    player_hand.remove(selected_card)   # Remove after it's moved
                    player.play_card(selected_card_str)

                    # Computer's turn
                    computer_card = random.choice(computer_hand)
                    computer_card_str = f"{computer_card.value}{computer_card.suit[0].upper()}"
                    computer_card.rect.topleft = (screen.get_width() // 2 - 160, screen.get_height() // 2)
                    computer.play_card(computer_card_str)
                    played_computer_card = computer_card
                    computer_hand.remove(computer_card)
                   
                    round_phase = "cards_revealed"
                    phase_timer = pygame.time.get_ticks() + 1500
                    # Resolve round
                    
        if round_phase == "cards_revealed" and pygame.time.get_ticks() > phase_timer:
            round_outcome = game.resolve_round(int(selected_card.value), int(computer_card.value), int(center_figure_card.value))
            round_phase = "result_display"
            phase_timer = pygame.time.get_ticks() + 1500
                    
        elif round_phase == "result_display" and pygame.time.get_ticks() > phase_timer:
            selected_card = None
            computer_card = None
            played_player_card = None
            played_computer_card = None
            round_outcome = None

            if figure_cards:
                next_figure = figure_cards.popleft()
                center_figure_card.image = pygame.image.load(get_figure_image_path(next_figure[0]))
                center_figure_card.image = pygame.transform.scale(center_figure_card.image, (FIGURE_CARD_WIDTH, FIGURE_CARD_HEIGHT))
                center_figure_card.value = next_figure[1]
                center_figure = next_figure
            else:
                game_is_running = False
                    
                    
                    # Check for win condition
                    # Updated winner check using Game method
            if player.score >= 91 or computer.score >= 91:
                game.declare_winner()  # Handles print logic
                pygame.display.flip()
                pygame.time.wait(10000)
                return
                    
            round_phase = "waiting_for_play"
                     
        # Draw visual elements
        for card in player_hand:
            card.draw(screen)
        for card in computer_hand:
            card.draw(screen)

        center_figure_card.draw(screen)

        if played_player_card:
            played_player_card.draw(screen)
        if played_computer_card:
            played_computer_card.draw(screen)
   
        # Result message
        if round_outcome:
            font = pygame.font.SysFont(None, 36)
            result_text = font.render(round_outcome, True, GOLD)
            screen.blit(result_text, (screen.get_width() // 2 - 120, 250))

        # Round label
        font = pygame.font.SysFont(None, 28)
        label = font.render("Round Card", True, GOLD)
        screen.blit(label, (center_figure_card.rect.centerx - 40, center_figure_card.rect.top - 25))

        # Scoreboard
        font = pygame.font.SysFont(None, 32)
        round_number = 18 - len(player.hand)
        score_line = f"Round: {round_number} | You: {player.score}   CPU: {computer.score}   Skips Left: {player.skips_left}"
        score_text = font.render(score_line, True, WHITE)
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 10))

        # Warnings
        if warning:
            font = pygame.font.SysFont(None, 30)
            warning_text = font.render(warning, True, (255, 0, 0))
            screen.blit(warning_text, (screen.get_width() // 2 - 180, 650))

        pygame.display.flip()

        

run_game(center_figure, figure_cards)
pygame.quit()
sys.exit()
