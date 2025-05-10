# Work To Do: handle specical rules + add background audio
import math # for the warning
import pygame
import random
from game_logic.deck import Deck
from game_logic.Player import Player
from game_logic.game import Game
from game_logic.Computer_AI import ComputerAI

from collections import defaultdict
import sys  # for quiting the game once its over

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

# poker table colour
green = (33, 124, 66)


class GameUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Get 'Em")

    def displayWelcomeScreen(self):
        self.screen.fill(green)
        font = pygame.font.SysFont(None, 40)

        welcome_message = ["\n****** Get 'Em Card Game ******",
                           "You vs Computer - good luck!",
                           "Highest card wins each round - simple!",
                           "Press key to start"]

        for i, line in enumerate(welcome_message):
            text = font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, 240 + i * 60))
            self.screen.blit(text, text_rect)

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

    def select_difficulty_screen(self):
        self.screen.fill(green)
        font_title = pygame.font.SysFont('arial', 60)
        font_button = pygame.font.SysFont('arial', 40)
    
        # the title
        title_text = "Select Difficulty Level"
        title_surf = font_title.render(title_text, True, GOLD)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        
        # the buttons with hover effects
        levels = ["Easy", "Normal", "Hard"]
        buttons = []
        for i, level in enumerate(levels):
            btn_rect = pygame.Rect(400, 200 + i * 120, 400, 80)
            buttons.append((btn_rect, level))
    
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            self.screen.fill(green)
            self.screen.blit(title_surf, title_rect)
            
            for rect, label in buttons:
                is_hover = rect.collidepoint(mouse_pos)
                color = LIGHT_BLUE if is_hover else BLUE
                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                pygame.draw.rect(self.screen, WHITE, rect, 3, border_radius=10)
                
                text = font_button.render(label, True, WHITE)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, level in buttons:
                        if rect.collidepoint(event.pos):
                            return level.lower()


game_ui = GameUI()
game_ui.displayWelcomeScreen()
difficulty = game_ui.select_difficulty_screen()
ai = ComputerAI(mode=difficulty)


def announce_winner(champion):
    """tells everyone who won at the end"""
    # trophy emoji makes it more apiling
    print(f"\n🏆 WINNER: {champion}!! 🏆")
    # extra line just because
    print("Thanks for playing!\n")


# Creating a window(The playing area):
screen = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Get 'Em ")

# coloring the playing area
green = (10, 110, 10)

# cards size and colour
CARD_WIDTH = 60
CARD_HEIGHT = 90
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

# figure cards size
FIGURE_CARD_WIDTH = 70
FIGURE_CARD_HEIGHT = 105


class Card:
    def __init__(self, position_x, position_y, value, suit=None, image_filename=None, width=CARD_WIDTH,
                 height=CARD_HEIGHT, border_color=BLACK):
        # set the card position and size relative to the screen
        self.rect = pygame.Rect(position_x, position_y, width, height)

        self.value = value  # stores card's value
        self.suit = suit  # tores card's suit
        self.border_color = border_color
        
        # load image, if not found, create a fallback drawing (backup case)
        if image_filename is not None:
            self.image =  pygame.image.load(image_filename)
            self.image =  pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        else:
            self.image = None

    def draw(self, screen):
        #adding a shadow effect
        shadow_offset = 3
        shadow_rect = self.rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        pygame.draw.rect(screen, (0, 0, 0, 128), shadow_rect)

        # adding a gold border  
        if self.border_color == GOLD:
            glow_rect = self.rect.inflate(8, 8)
            pygame.draw.rect(screen, (255, 223, 128), glow_rect, border_radius=10)
            pygame.draw.rect(screen, GOLD, self.rect, 3, border_radius=8)
        else:
            pygame.draw.rect(screen, WHITE, self.rect, border_radius=8)
            pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=8)

        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            # drawing the card 
            pygame.draw.rect(screen, WHITE, self.rect, border_radius=8)
            font = pygame.font.SysFont('arial', 30)
            text = font.render(f"{self.value} {self.suit[0].upper()}", True, BLACK)
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
random.shuffle(cards)  # maybe delete this?
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

player = Player("You")
computer = Player("Computer")

"""player.hand = player_cards  # Assign the list of 18 cards
computer.hand = computer_cards
player.hand = [f"{val}{suit[0].upper()}" for val, suit in player_cards] """ # I deleted because it's duplicated codes and casue errors

# We give the computer the actual Card objects (used in UI)
game = Game()
game.player = player
game.computer = computer

game.players = [game.player, game.computer]
ui_player_cards   = []
ui_computer_cards = []
game.player.hand   = [f"{val}{suit[0].upper()}" for val, suit in player_cards]
game.computer.hand = [f"{val}{suit[0].upper()}" for val, suit in computer_cards]

# fill player and computer hands with Card objects
ui_player_cards = []
ui_computer_cards = []
for idx, (value, suit) in enumerate(player_cards):
    x = start_x + (idx % 9) * (CARD_WIDTH + card_spacing)
    y = 500 + (idx // 9) * (CARD_HEIGHT + 10)
    image_path = get_card_image_path(value, suit)
    card = Card(x, y, value, suit, image_path)
    ui_player_cards.append(card)

for idx, (value, suit) in enumerate(computer_cards):
    x = start_x + (idx % 9) * (CARD_WIDTH + card_spacing)
    y = 33 + (idx // 9) * (CARD_HEIGHT + 10)
    image_path = get_card_image_path(value, suit)
    card = Card(x, y, value, suit, image_path)
    ui_computer_cards.append(card)
# initialize computer_string_hand with the correct values
computer_string_hand = [f"{val}{suit[0].upper()}" for val, suit in computer_cards]

# update AI player hand with string version
computer.hand = computer_string_hand
ai = ComputerAI(mode=difficulty)

figure_cards = deck.create_figure_cards()  # shuffled list of figure cards(imported from the deck class)
center_figure = deck.draw_figure_card()  # pick one figure card from the top


# Helper function to turn figure code like 'QD' into a usable image path
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


center_image_path = get_figure_image_path(center_figure[0])  # Get the figure card image path

# Center the figure card + Add gold border around the figure card
GOLD = (255, 215, 0)

center_figure_card = Card(
    565, 290,  # Position
    center_figure[1],  # Value
    suit=None,
    image_filename=center_image_path,
    width=FIGURE_CARD_WIDTH,  # Bigger size
    height=FIGURE_CARD_HEIGHT,
    border_color=GOLD  # Gold border
)


# Converts string like "7H" to a card-like object with .value, .suit, .code
class SimpleCard:
    def __init__(self, code):
        self.code = code
        self.value = int(code[:-1])
        self.suit = code[-1]


def build_computer_hand_objects(card_strs):
    return [SimpleCard(c) for c in card_strs]


round_in_progress = False
round_ended = False
round_end_time = 0
SKIP_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - 20, SCREEN_HEIGHT - BUTTON_HEIGHT - 20, BUTTON_WIDTH,
                               BUTTON_HEIGHT)


def run_game(center_figure, figure_cards, ai):
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

    while game_is_running:
        screen.fill(green)

        if warning and pygame.time.get_ticks() > warning_timer:
            warning = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SKIP_BUTTON_RECT.collidepoint(event.pos) and round_phase == "waiting_for_play":
                    if figure_cards:
                        next_figure = figure_cards.popleft()
                        center_figure_card.image = pygame.image.load(get_figure_image_path(next_figure[0]))
                        center_figure_card.image = pygame.transform.scale(center_figure_card.image,
                                                                          (FIGURE_CARD_WIDTH, FIGURE_CARD_HEIGHT))
                        center_figure_card.value = next_figure[1]
                        center_figure = next_figure
                    else:
                        game_is_running = False
                    continue

            if round_phase == "waiting_for_play" and event.type == pygame.MOUSEBUTTONDOWN and not selected_card:
                mouse_pos = pygame.mouse.get_pos()

                for card in ui_player_cards:  # changed from player_cards to ui_player_cards
                    if card.rect.collidepoint(mouse_pos):
                        selected_card = card
                        selected_card_str = f"{card.value}{card.suit[0].upper()}"
                        selected_card.rect.topleft = (screen.get_width() // 2 + 100, screen.get_height() // 2)
                        break

                if selected_card:
                    # check if selected card is in player's hand
                    if selected_card_str not in player.hand:
                        warning = "Card not in hand!"
                        warning_timer = pygame.time.get_ticks() + 3000
                        selected_card = None
                        continue
                    # special card logic
                    if selected_card_str in ['2S', '9S']:
                        player.used_special = True
                        player.last_special = selected_card_str
                    else:
                        if player.last_special in ["2S", "9S"] and selected_card.value in ["3", "9"]:
                            warning = "You can't play 3 or 10 after 2S or 9S!"
                            warning_timer = pygame.time.get_ticks() + 3000
                            selected_card = None
                            continue

                    # remove from both hands
                    selected_card.rect.topleft = (screen.get_width() // 2 + 100, screen.get_height() // 2)
                    played_player_card = selected_card
                    ui_player_cards.remove(selected_card)  #changed from player_hand to ui_player_cards
                    player.play_card(selected_card_str)

                    # update AI hand
                    game.computer.hand = [f"{card.value}{card.suit[0].upper()}" for card in ui_computer_cards]
                    print("AI hand before playing:", game.computer.hand)
                    print("UI computer_hand (visible):",
                          [f"{card.value}{card.suit[0].upper()}" for card in ui_computer_cards])

                    game.current_figure = center_figure
                    computer_card_obj = ai.play(game)
                    print("AI played:", computer_card_obj)
                    
                    # get the computer card string
                    computer_card_str = None
                    if isinstance(computer_card_obj, str):
                        computer_card_str = computer_card_obj
                    elif hasattr(computer_card_obj, "code"):
                        computer_card_str = computer_card_obj.code
                    elif computer_card_obj is None:
                        # if AI cant play, pick the first available card as fallback
                        if ui_computer_cards:
                            first_card = ui_computer_cards[0]
                            computer_card_str = f"{first_card.value}{first_card.suit[0].upper()}"
                    
                    # only proceed if we have a valid card string
                    if computer_card_str:
                        # find the matching Card object from computers hand
                        for card in ui_computer_cards:
                            card_code = f"{card.value}{card.suit[0].upper()}"
                            if card_code == computer_card_str:
                                computer_card = card
                                played_computer_card = card
                                ui_computer_cards.remove(card)
                                card.rect.topleft = (screen.get_width() // 2 - 160, screen.get_height() // 2)
                                # remove the card from computers hand
                                if computer_card_str in game.computer.hand:
                                    game.computer.hand.remove(computer_card_str)
                                break
                    
                    # computers turn result
                    if computer_card:
                        round_phase = "cards_revealed"
                        phase_timer = pygame.time.get_ticks() + 1500
                    else:
                        # if AI failed to play show message and continue game
                        warning = "Computer skips turn"
                        warning_timer = pygame.time.get_ticks() + 3000
                        round_phase = "cards_revealed"
                        phase_timer = pygame.time.get_ticks() + 1500

                    round_phase = "cards_revealed"
                    phase_timer = pygame.time.get_ticks() + 1500
                    # resolve round

        if round_phase == "cards_revealed" and pygame.time.get_ticks() > phase_timer:
            player_card_str = f"{selected_card.value}{selected_card.suit[0].upper()}"
            computer_card_str = f"{computer_card.value}{computer_card.suit[0].upper()}"
            round_outcome = game.play_round(player_card_str, computer_card_str, center_figure)
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
                center_figure_card.image = pygame.transform.scale(center_figure_card.image,
                                                                  (FIGURE_CARD_WIDTH, FIGURE_CARD_HEIGHT))
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
        for card in ui_player_cards:
            card.draw(screen)
        for card in ui_computer_cards:
            card.draw(screen)

        center_figure_card.draw(screen)

        if played_player_card:
            played_player_card.draw(screen)
        if played_computer_card:
            played_computer_card.draw(screen)

        # round outcome results
        if round_outcome:
            font = pygame.font.SysFont('arial', 48)  # increasing the font
            result_text = font.render(round_outcome, True, GOLD)
            # adding a  transparent background with a glow effect
            text_surface = pygame.Surface((result_text.get_width() + 40, result_text.get_height() + 20), pygame.SRCALPHA)
            glow_color = (255, 223, 128, 100)
            pygame.draw.rect(text_surface, glow_color, text_surface.get_rect(), border_radius=15)
            text_surface.blit(result_text, (20, 10))
            screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2, 180))

        #  round card title design 
        font = pygame.font.SysFont('arial', 24)  # the perfect size
        label = font.render("Round Card", True, GOLD)
        # adding a background to the title with a glow effect.        
        label_bg = pygame.Surface((label.get_width() + 20, label.get_height() + 10), pygame.SRCALPHA)
        pygame.draw.rect(label_bg, (0, 0, 0, 200), label_bg.get_rect(), border_radius=8)
        # adding a golden frame
        pygame.draw.rect(label_bg, GOLD, label_bg.get_rect(), 1, border_radius=8)
        label_bg.blit(label, (10, 5))  # modify the position of text
        screen.blit(label_bg, (center_figure_card.rect.centerx - label_bg.get_width() // 2, 
                              center_figure_card.rect.top - 30)) # adjust the position slightly upwards

        # design of the scoreboard at the top 
        font = pygame.font.SysFont('arial', 25)  # making it a lil smaller (bigger is not always better)
        round_number = 10 - len(player.hand)
        score_line = f"Round: {round_number} | You: {player.score}  CPU: {computer.score}  Skips: {player.skips_left}"
        score_text = font.render(score_line, True, WHITE)
        
        # the background
        score_bg = pygame.Surface((score_text.get_width() + 30, score_text.get_height() + 10), pygame.SRCALPHA)
        gradient_color = (0, 0, 0, 230)
        pygame.draw.rect(score_bg, gradient_color, score_bg.get_rect(), border_radius=15)
        pygame.draw.rect(score_bg, GOLD, score_bg.get_rect(), 2, border_radius=15)
        score_bg.blit(score_text, (20, 7))  # setting where the text is
        screen.blit(score_bg, (screen.get_width() // 2 - score_bg.get_width() // 2, 10))

        """# the round card announcement 
        font = pygame.font.SysFont('arial', 20)  #making it a lil smaller (bigger is not always better)
        label = font.render("Round Card", True, GOLD)
        label_bg = pygame.Surface((label.get_width() + 30, label.get_height() + 15), pygame.SRCALPHA)
        
        
        screen.blit(label_bg, (center_figure_card.rect.centerx - label_bg.get_width() // 2, 
                              center_figure_card.rect.top - 35))  # moving it a lil to the top"""

        # the skip button 
        skip_color = (200, 0, 0) if round_phase == "waiting_for_play" else (150, 0, 0)
        shadow_rect = SKIP_BUTTON_RECT.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(screen, (50, 0, 0), shadow_rect, border_radius=15)
        pygame.draw.rect(screen, skip_color, SKIP_BUTTON_RECT, border_radius=15)
        pygame.draw.rect(screen, WHITE, SKIP_BUTTON_RECT, 2, border_radius=15)
        
        font = pygame.font.SysFont('arial', 34)
        skip_text = font.render("SKIP", True, WHITE)
        skip_text_rect = skip_text.get_rect(center=SKIP_BUTTON_RECT.center)
        screen.blit(skip_text, skip_text_rect)

        #the warning message 
        if warning:
            font = pygame.font.SysFont('arial', 36)
            warning_text = font.render(warning, True, (255, 50, 50))
            # adding a glow effect when getting a warning
            warning_alpha = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 128 + 127
            warning_bg = pygame.Surface((warning_text.get_width() + 40, warning_text.get_height() + 20), pygame.SRCALPHA)
            warning_color = (0, 0, 0, int(warning_alpha))
            pygame.draw.rect(warning_bg, warning_color, warning_bg.get_rect(), border_radius=12)
            warning_bg.blit(warning_text, (20, 10))
            screen.blit(warning_bg, (screen.get_width() // 2 - warning_bg.get_width() // 2, 600))

        pygame.display.flip()


run_game(center_figure, figure_cards, ai)
pygame.quit()
sys.exit()
