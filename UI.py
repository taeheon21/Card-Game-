import pygame

import random
from deck import Deck

import sys # for quiting the game once its over

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

class Card:
    def __init__(self, position_x, position_y ,value,suit=None,image_filename=None): 
        #set the card position and size relative to the screen
        self.rect = pygame.Rect(position_x, position_y, CARD_WIDTH, CARD_HEIGHT)
        
        self.value = value#stores card's value (e.g. 2,5,...)
        self.suit = suit    # e.g., "hearts", "clubs"

        #load image, if not found, create a fallback drawing (backup case)
        if image_filename is not None:
            self.image = pygame.image.load(image_filename)
            self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        else:
            self.image = None

    def draw(self, screen): 
        # Draw the card image at its designated position
        if self.image:
            screen.blit(self.image, self.rect.topleft)
             # draw a black border around the image; clarity
            pygame.draw.rect(screen, BLACK, self.rect, 1)  # 1 = border thickness

        else:
            # fallback if image is missing
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
player_hand = []  # holds all 18 Card objects

# Deal 18 cards from the deck to the player
for i in range(18):
    value = deck.draw_card()  # Get a card value (2–10)
# Get a random suit from the deck's suit list
    suit = random.choice(deck.suits)  
    image_path = get_card_image_path(value, suit)  # Get the image path for that value and suit
    x = 50 + (i % 9) * (CARD_WIDTH + 10)     # Column position (9 cards per row)
    y = 500 + (i // 9) * (CARD_HEIGHT + 10)  # Row 1 or 2
    card = Card(x, y, value, suit,image_path)
    player_hand.append(card)

# The Game loop
game_is_running = True

while game_is_running:
    screen.fill(green)

    for event in pygame.event.get(): #checking for any actions a player takes
        if event.type == pygame.QUIT: # Do they press the 'exit' button?
            game_is_running = False # quit if yes
            
    for card in player_hand:
        card.draw(screen)


    pygame.display.flip()
pygame.quit()
sys.exit()

"""
golden borders for special cards:
BORDER_COLOR = (255, 215, 0)  # Gold!
pygame.draw.rect(screen, BORDER_COLOR, self.rect, 3)
"""
