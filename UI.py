import pygame
import sys # for quiting the game once its over

from deck import Deck
from collections import defaultdict

import random

pygame.init()

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
#figure cards size
FIGURE_CARD_WIDTH = 70
FIGURE_CARD_HEIGHT = 105


class Card:
    def __init__(self, position_x, position_y ,value,suit=None,image_filename=None,width=CARD_WIDTH, height=CARD_HEIGHT, border_color=BLACK):
        #set the card position and size relative to the screen
        self.rect = pygame.Rect(position_x, position_y, width, height)
        
        self.value = value #stores card's valu
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

deck = Deck()  # Create a new shuffled deck
 

grouped_cards = defaultdict(list)
suits = ['hearts', 'diamonds', 'spades', 'clubs']
value_counts = {}

# Build 36 (value, suit) pairs manually using the values from the deck
all_values = deck.cards.copy()
random.shuffle(all_values)

for value in all_values:
    count = value_counts.get(value, 0)
    if count < 4:
        suit = suits[count]
        grouped_cards[value].append((value, suit))
        value_counts[value] = count + 1


player_values = []
computer_values = []

for value in range(2, 11):  # For each value 2–10
    suits = grouped_cards[value]

    # Just in case, shuffle again to randomize suit order
    random.shuffle(suits)

    # First 2 to player, last 2 to computer
    player_values.extend(suits[:2])
    computer_values.extend(suits[2:])

player_hand = []
computer_hand = []

player_cards = player_values
computer_cards = computer_values

card_spacing = 6
total_width = (CARD_WIDTH * 9) + (card_spacing * 8)
start_x = (screen.get_width() - total_width) // 2


    
for i, (value, suit) in enumerate(player_cards):
        x = start_x + (i % 9) * (CARD_WIDTH + card_spacing)
        y = 500 + (i // 9) * (CARD_HEIGHT + 10) 
        image_path = get_card_image_path(value, suit)  # Get the image path for that value and suit
        player_hand.append(Card(x, y, value, suit, image_path))

for i, (value, suit) in enumerate(computer_cards):
        x = start_x + (i % 9) * (CARD_WIDTH + card_spacing)
        y = 35 + (i // 9) * (CARD_HEIGHT + 10) 
        image_path = get_card_image_path(value, suit)  # Get the image path for that value and suit
        computer_hand.append(Card(x, y, value, suit, image_path))

figure_cards = deck.create_figure_cards() # shuffled list of figure cards(imported from the deck class)
center_figure = figure_cards.popleft()  # pick one figure card from the top


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


# The Game loop
game_is_running = True

while game_is_running:
    screen.fill(green)

    for event in pygame.event.get(): #checking for any actions a player takes
        if event.type == pygame.QUIT: # Do they press the 'exit' button?
            game_is_running = False # quit if yes
            
    for card in player_hand:
        card.draw(screen)
    
    for card in computer_hand:
        card.draw(screen)

    center_figure_card.draw(screen) # Draw center figure card

    font = pygame.font.SysFont(None, 28)
    label = font.render("Round Card", True, GOLD)
    screen.blit(label, (center_figure_card.rect.centerx - 40, center_figure_card.rect.top - 25))


    pygame.display.flip()
pygame.quit()
sys.exit()