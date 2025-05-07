#a new deck mid-game (e.g. redistributing):
# game.deck.redistribute_number_cards()

import pygame
import random
import sys # for quiting the game once its over

from game_logic.deck import Deck
from game_logic.Player import Player
from game_logic.game import Game

# === Game Constants ===5667929
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 40
MARGIN, FPS = 20, 30

# === Colors === 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
LIGHT_BLUE = (100, 100, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)

# poker table colour:test it
green = (33, 124, 66)

#numberd cards size 
CARD_WIDTH = 60
CARD_HEIGHT = 90

#figure cards size
FIGURE_CARD_WIDTH = 90
FIGURE_CARD_HEIGHT = 130
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Get 'Em")
#5667929

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
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = None

    def draw(self, screen): 

        # Create a slightly bigger golden rectangle for figure cards
        if self.border_color == (255, 215, 0):  # GOLD
            border_rect = self.rect.inflate(10, 10)
            border_rect.center = self.rect.center  # Ensure it's centered
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
    suit_map = {
        'H': 'hearts',
        'D': 'diamonds',
        'S': 'spades',
        'C': 'clubs'
    }
    suit_str = suit_map.get(suit.upper(), suit.lower())
    return f"assets/cards/png/{value_str}_of_{suit_str}.png"

card_spacing = 6
total_width = (CARD_WIDTH * 9) + (card_spacing * 8)
start_x = (screen.get_width() - total_width) // 2

game = Game()
deck = game.deck
game.deal_cards()

player = game.players[0]
computer = game.players[1]

player_hand = []
computer_hand = []

# Fill player and computer hands
for plyer, card_str in enumerate(player.hand):
        value, suit = card_str[:-1], card_str[-1]
        x = start_x + (plyer  % 9) * (CARD_WIDTH + card_spacing)
        y = 500  + (plyer // 9) * (CARD_HEIGHT + 10)
        image_path = get_card_image_path(value, suit)
        player_hand.append(Card(x, y, value, suit, image_path))

for comp, card_str in enumerate(computer.hand):   
        value, suit = card_str[:-1], card_str[-1]
        x = start_x + (comp % 9) * (CARD_WIDTH + card_spacing)
        y = 33 + (comp // 9) * (CARD_HEIGHT + 10)
        image_path = get_card_image_path(value, suit)
        computer_hand.append(Card(x, y, value, suit, image_path))

#5667929
figure_cards = game.deck.figure_cards
center_figure = game.deck.draw_figure_card()
game.current_figure = center_figure  # this way game.py knows which figure card is active
#5667929

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

#Center the figure card exactly in the center!
center_x = SCREEN_WIDTH // 2 - FIGURE_CARD_WIDTH // 2
center_y = SCREEN_HEIGHT // 2 - FIGURE_CARD_HEIGHT // 2

center_figure_card = Card(
    center_x , center_y,                          # Position
    center_figure[1],                 # Value
    suit=None,
    image_filename=center_image_path,
    width=FIGURE_CARD_WIDTH,          # Bigger size
    height=FIGURE_CARD_HEIGHT,
    border_color=GOLD                 # Gold border
)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Get 'Em")

running = True
while running:
    screen.fill(green)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw all cards
    for card in player_hand:
        card.draw(screen)

    for card in computer_hand:
        card.draw(screen)

    center_figure_card.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
'''
class GameUI:
    def __init__(self,game):
        self.game = game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Get 'Em Card Game")
        self.clock = pygame.time.Clock()

    def displayWelcomeScreen(self):
        self.screen.fill(green)
        font = pygame.font.SysFont(None, 40)

        welcome_message= ["** Get 'Em Card Game **",
        "Good Luck!",
        "Highest Card Wins Each Round - Simple!"]

        for i, line in enumerate(welcome_message):
            text = font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, 240 + i * 60))
            self.screen.blit(text, text_rect)

        pygame.display.flip()
    # Waitint for the user to press the key/button??!
    def starting_the_game(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                   return
    
    def render(self, final=False):
        self.screen.fill(GREEN)
        self.draw_scores()

        # Draw computer hand
        self.draw_hand(self.game.players[1].hand, top=True)

        # Draw player hand
        self.draw_hand(self.game.players[0].hand, top=False)

        # Draw figure card if exists
        if self.game.current_figure:
            fig_code = self.game.current_figure[0]
            val = self.game.current_figure[1]
            image_path = self.get_figure_image_path(fig_code)
            self.draw_card(565, 290, val, None, image_path, FIGURE_CARD_WIDTH, FIGURE_CARD_HEIGHT, GOLD)
            label = self.font.render("Round Card", True, YELLOW)
            self.screen.blit(label, (560, 270))

        pygame.display.flip()
    
    #This is the main game loop (ensures the game continues till the winning condition is met)           
    def run(self):
        self.display_welcome_screen()
        while not self.game.game_over():#if the winning condition is not met
            self.render()
            self.game.play_round()# continue for the next round
            pygame.time.delay(1500)

        self.render(final=True) #final board state
        pygame.time.delay(4000) #time to read the results

game_ui = GameUI()
game_ui.displayWelcomeScreen()
#Handle guit operation
running = True
while running:
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
'''