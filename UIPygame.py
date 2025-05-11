import math  # for the warning
import pygame
import random
import os 
from game_logic.deck import Deck
from game_logic.Player import Player
from game_logic.game import Game
from game_logic.Computer_AI import ComputerAI

from collections import defaultdict
import sys  # for quiting the game once its over

#5667929:
# === Game Constants ===
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 40
MARGIN, FPS = 20, 30
MUSIC_VOLUME = 0.3  
# cards size and colour
CARD_WIDTH = 60
CARD_HEIGHT = 90

# figure cards size
FIGURE_CARD_WIDTH = 70
FIGURE_CARD_HEIGHT = 105

# === Colors ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (20, 140, 70)
RED = (150, 10, 10)
BLUE = (0, 0, 200)
LIGHT_BLUE = (100, 100, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
YELLOW = (210, 180, 60)
GOLD = (255, 215, 0)
# poker table colour:5640968
green = (33, 124, 66)

#5667929:
# function to draw background
def draw_background(screen, background=None):
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(green)

# function to load and play background music
def load_background_music():
    music_folder = os.path.join("assets", "sounds")
    # the  music file
    music_file = "game music.mp3"
    music_path = os.path.join(music_folder, music_file)
    
    if not os.path.exists(music_path):
        print(f"Music file not found: {music_path}")
        return False
    
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        print(f"Now playing: {music_file}")
        return True
    except pygame.error as e:
        print(f"Error loading music: {e}")
        return False
#5667929.

#5640968:
class GameUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Get 'Em")
#5640968.
#5667929:
        # loading the background image:
        background_path = os.path.join("assets", "cards", "poker_table.jpg")
        try:
            self.background = pygame.image.load(background_path)
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
                print(f"Could not load background image: {background_path}")
                print("Using solid color instead")
                self.background = None
        
        # load background music
        self.music_playing = load_background_music()
       
    # toggle music 
    def toggle_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            return False
        else:
            pygame.mixer.music.unpause()
            return True

    def displayWelcomeScreen(self):
        draw_background(self.screen, self.background)
        font = pygame.font.SysFont(None, 40)

        welcome_message = ["\n****** Get 'Em Card Game ******",
                           "You vs Computer - good luck!",
                           "Highest card wins each round - simple!",
                           "Press key to start",
                           "",
                           "M = Toggle Music"]  
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
                    if event.key == pygame.K_m:  # m key toggles music
                        self.music_playing = self.toggle_music()
                    else:
                        waiting = False
#5667929.
#5640968:
# This function allows the user to select the AI level they want to play against
    def select_difficulty_screen(self):
        draw_background(self.screen, self.background)
        font_title = pygame.font.SysFont('arial', 50)
        font_button = pygame.font.SysFont('arial', 40)

        # the title
        title_text = "Select the AI Difficulty Level: "
        title_surface = font_title.render(title_text, True, GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 160))

        # the buttons with hover effects
        levels = [("Easy", GREEN), ("Normal", YELLOW), ("Hard", RED)]  #Assigning different color value for each button 
        buttons = []
        for i, (label, color) in enumerate(levels):
            btn_rect = pygame.Rect(440, 300 + i * 100, 280, 60)
            buttons.append((btn_rect, label, color))

        while True:
            mouse_pos = pygame.mouse.get_pos()

            draw_background(self.screen, self.background)
            self.screen.blit(title_surface, title_rect)

            for rect, label, color in buttons:
                is_hover = rect.collidepoint(mouse_pos)
                fill_color = LIGHT_BLUE if is_hover else color
                pygame.draw.rect(self.screen, fill_color, rect, border_radius=10)
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
                    for rect, label, color in buttons:
                        if rect.collidepoint(event.pos):
                            return label.lower()


game_ui = GameUI()
game_ui.displayWelcomeScreen()
difficulty = game_ui.select_difficulty_screen()
ai = ComputerAI(mode=difficulty)
#5640968.
#5640968:
# Creating a window(The playing area):
screen = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Get 'Em ")

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
            self.image = pygame.image.load(image_filename)
            self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        else:
            self.image = None

    def draw(self, screen):
        # adding a shadow effect
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

# We give the computer the actual Card objects (used in UI)
game = Game()
game.player = player
game.computer = computer

game.players = [game.player, game.computer]
ui_player_cards = []
ui_computer_cards = []
game.player.hand = [f"{val}{suit[0].upper()}" for val, suit in player_cards]
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

center_figure_card = Card(
    565, 290,  # Position
    center_figure[1],  # Value
    suit=None,
    image_filename=center_image_path,
    width=FIGURE_CARD_WIDTH,  # Bigger size
    height=FIGURE_CARD_HEIGHT,
    border_color=GOLD  # Gold border
)

round_in_progress = False
round_ended = False
round_end_time = 0
SKIP_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - 20, SCREEN_HEIGHT - BUTTON_HEIGHT - 20, BUTTON_WIDTH,
                               BUTTON_HEIGHT)
#5640968.

def run_game(center_figure, figure_cards, ai): #5640968: All by Yaqin, Except for the mentioned parts below.
    game_is_running = True
    skip_count = 0
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
    skips_allowed = 2
    skips_used = 0
    
    # get the background from the game_ui instance
    background = game_ui.background if hasattr(game_ui, 'background') else None

    # Added for tracking tie state (5676101)
    tie_break_cards = []  # Cards played during tie
    in_tiebreak = False

    while game_is_running:
        draw_background(screen, background)  # use the background image instead of fill

        if warning and pygame.time.get_ticks() > warning_timer:
            warning = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SKIP_BUTTON_RECT.collidepoint(event.pos) and round_phase == "waiting_for_play":
                    if skips_used < skips_allowed:
                        player.skips_left -= 1  # taeheon
                        skip_count += 1
                        computer_choice = random.choice(game.computer.hand)  # Computer choose card randomly
                        for card in ui_computer_cards:
                            card_str = f"{card.value}{card.suit[0].upper()}"
                            if card_str == computer_choice:
                                played_computer_card = card
                                ui_computer_cards.remove(card)
                                card.rect.topleft = (screen.get_width() // 2 - 160, screen.get_height() // 2)
                                break
                        round_outcome = game.skip_round(computer_choice,
                                                        center_figure)  # using game class(skip_round) and sort it out
                        round_phase = "result_display"
                        phase_timer = pygame.time.get_ticks() + 1500  # taeheon

                        if figure_cards:
                            next_figure = figure_cards.popleft()
                            center_figure_card.image = pygame.image.load(get_figure_image_path(next_figure[0]))
                            center_figure_card.image = pygame.transform.scale(center_figure_card.image,
                                                                              (FIGURE_CARD_WIDTH, FIGURE_CARD_HEIGHT))
                            center_figure_card.value = next_figure[1]
                            center_figure = next_figure
                            skips_used += 1
                        else:
                            game_is_running = False
                        continue
                    else:
                        warning = "NO skips left!"
                        warning_timer = pygame.time.get_ticks() + 1500
                    continue

            if round_phase == "waiting_for_play" and event.type == pygame.MOUSEBUTTONDOWN and not selected_card:
                mouse_pos = pygame.mouse.get_pos()

                for card in ui_player_cards:  # changed from player_cards to ui_player_cards
                    if card.rect.collidepoint(mouse_pos):
                        selected_card_str = f"{card.value}{card.suit[0].upper()}"
                        if selected_card_str not in player.hand:
                            warning = "Card not in hand!"
                            warning_timer = pygame.time.get_ticks() + 3000
                            continue
                        if card.value in ["3", "10"] and player.last_special in ["2S", "9S"]:
                            warning = "You can't play 3 or 10 after 2S or 9S!"
                            warning_timer = pygame.time.get_ticks() + 3000
                            selected_card = None
                            played_player_card = None
                            continue
                        else:
                            # Allowing the player to chose another card
                            selected_card = card
                            played_player_card = card
                            ui_player_cards.remove(card)
                            player.play_card(selected_card_str)
                            card.rect.topleft = (screen.get_width() // 2 + 100, screen.get_height() // 2)

                            # special card logic
                            if selected_card_str in ['2S', '9S']:
                                player.used_special = True
                                player.last_special = selected_card_str
                            else:
                                player.last_special = None
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
                            if ui_computer_cards is None and ui_computer_cards:
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
                        round_phase = "cards_revealed"
                        phase_timer = pygame.time.get_ticks() + 1500
                        break
                    # resolve round

        if round_phase == "cards_revealed" and pygame.time.get_ticks() > phase_timer:
            if selected_card:
                if selected_card.value in ["3", "10"] and player.last_special in ["2S", "9S"]:
                    warning = "Invalid move skipped!"
                    warning_timer = pygame.time.get_ticks() + 3000
                    selected_card = None
                    played_player_card = None
                    round_phase = "waiting_for_play"
                    continue

            if not selected_card or not computer_card:
                round_phase = "waiting_for_play"
                continue
            player_card_str = f"{selected_card.value}{selected_card.suit[0].upper()}"
            computer_card_str = f"{computer_card.value}{computer_card.suit[0].upper()}"

            # I made the following changes (5676101)
            round_outcome = game.play_round(player_card_str, computer_card_str, center_figure)

            # Check if it's a tie
            if "Tie" in round_outcome and not "resolved" in round_outcome:
                in_tiebreak = True
                tie_break_cards.append((played_player_card, played_computer_card))
                round_phase = "tiebreak_play"
                selected_card = None
                computer_card = None
                played_player_card = None
                played_computer_card = None
                round_outcome = "It's a tie! Play another card..."
                phase_timer = pygame.time.get_ticks() + 1500
            else:
                round_phase = "result_display"
                phase_timer = pygame.time.get_ticks() + 1500

        # Card selection logic for tiebreak (5676101)
        elif round_phase == "tiebreak_play" and event.type == pygame.MOUSEBUTTONDOWN and not selected_card:
            mouse_pos = pygame.mouse.get_pos()

            for card in ui_player_cards:
                if card.rect.collidepoint(mouse_pos):
                    selected_card_str = f"{card.value}{card.suit[0].upper()}"
                    if card.value in ["3", "10"] and player.last_special in ["2S", "9S"]:
                        warning = "You can't play 3 or 10 after 2S or 9S!"
                        warning_timer = pygame.time.get_ticks() + 3000
                        continue

                    # Play tiebreak card
                    selected_card = card
                    played_player_card = card
                    ui_player_cards.remove(card)
                    player.play_card(selected_card_str)
                    card.rect.topleft = (screen.get_width() // 2 + 100, screen.get_height() // 2)

                    # Computer plays tiebreak card
                    game.computer.hand = [f"{card.value}{card.suit[0].upper()}" for card in ui_computer_cards]
                    game.current_figure = center_figure
                    computer_card_obj = ai.play(game)

                    if isinstance(computer_card_obj, str):
                        computer_card_str = computer_card_obj
                    elif hasattr(computer_card_obj, "code"):
                        computer_card_str = computer_card_obj.code
                    else:
                        computer_card_str = None

                    if computer_card_str:
                        for card in ui_computer_cards:
                            card_code = f"{card.value}{card.suit[0].upper()}"
                            if card_code == computer_card_str:
                                computer_card = card
                                played_computer_card = card
                                ui_computer_cards.remove(card)
                                card.rect.topleft = (screen.get_width() // 2 - 160, screen.get_height() // 2)
                                if computer_card_str in game.computer.hand:
                                    game.computer.hand.remove(computer_card_str)
                                break

                    # Resolve tiebreak
                    round_phase = "tiebreak_revealed"
                    phase_timer = pygame.time.get_ticks() + 1500
                    break

        # Tiebreak resolution handling (5676101)
        elif round_phase == "tiebreak_revealed" and pygame.time.get_ticks() > phase_timer:
            if selected_card and computer_card:
                player_card_str = f"{selected_card.value}{selected_card.suit[0].upper()}"
                computer_card_str = f"{computer_card.value}{computer_card.suit[0].upper()}"
                round_outcome = game.handle_tie2(player_card_str, computer_card_str, center_figure)

                # Check if still tied
                if "Tie" in round_outcome and not "resolved" in round_outcome:
                    tie_break_cards.append((played_player_card, played_computer_card))
                    # Do coin flip to resolve
                    round_outcome = game.resolve_tie_coinflip(center_figure)

                round_phase = "result_display"
                phase_timer = pygame.time.get_ticks() + 1500
                in_tiebreak = False

        elif round_phase == "result_display" and pygame.time.get_ticks() > phase_timer:
            selected_card = None
            computer_card = None
            played_player_card = None
            played_computer_card = None
            round_outcome = None
            tie_break_cards = []  # Added this
            in_tiebreak = False  # Added this

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
            if player.score >= 101 or computer.score >= 101 or  round_number >= 16:
                # annoucing the winner
                winner = "Player" if player.score >= computer.score else "AI"
                font = pygame.font.SysFont('arial', 72)
                winner_text = f"The winner: {winner}!"
                winner_surface = font.render(winner_text, True, GOLD)
                
                # background for the announcmient text
                winner_bg = pygame.Surface((winner_surface.get_width() + 60, winner_surface.get_height() + 40), pygame.SRCALPHA)
                pygame.draw.rect(winner_bg, (0, 0, 0, 200), winner_bg.get_rect(), border_radius=20)
                pygame.draw.rect(winner_bg, GOLD, winner_bg.get_rect(), 3, border_radius=20)
                winner_bg.blit(winner_surface, (30, 20))
                
                # the final score 
                score_font = pygame.font.SysFont('arial', 36)
                score_text = f"Final score : Player: {player.score} | AI: {computer.score}"
                score_surface = score_font.render(score_text, True, WHITE)
                score_bg = pygame.Surface((score_surface.get_width() + 40, score_surface.get_height() + 20), pygame.SRCALPHA)
                pygame.draw.rect(score_bg, (0, 0, 0, 180), score_bg.get_rect(), border_radius=15)
                score_bg.blit(score_surface, (20, 10))
                
                # displaying the winner and the score
                screen.blit(winner_bg, (screen.get_width() // 2 - winner_bg.get_width() // 2, 
                                      screen.get_height() // 2 - winner_bg.get_height() // 2))
                screen.blit(score_bg, (screen.get_width() // 2 - score_bg.get_width() // 2,
                                     screen.get_height() // 2 + winner_bg.get_height()))
                pygame.display.flip()
                pygame.time.wait(5000)
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
            text_surface = pygame.Surface((result_text.get_width() + 40, result_text.get_height() + 20),
                                          pygame.SRCALPHA)
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
                               center_figure_card.rect.top - 30))  # adjust the position slightly upwards

        # design of the scoreboard at the top
        font = pygame.font.SysFont('arial', 25)  # making it a lil smaller (bigger is not always better)
        round_number = 18 - len(player.hand) + skip_count + 1
        if round_number >= 18:  # taeheon
            game.declare_winner()
            pygame.display.flip()
            pygame.time.wait(5000)
            return  # taeheon

        score_line = f"Round: {round_number} | You: {player.score}  AI: {computer.score}  Skips: {player.skips_left}"
        score_text = font.render(score_line, True, WHITE)

        # the background
        score_bg = pygame.Surface((score_text.get_width() + 30, score_text.get_height() + 10), pygame.SRCALPHA)
        gradient_color = (0, 0, 0, 230)
        pygame.draw.rect(score_bg, gradient_color, score_bg.get_rect(), border_radius=15)
        pygame.draw.rect(score_bg, GOLD, score_bg.get_rect(), 2, border_radius=15)
        score_bg.blit(score_text, (20, 7))  # setting where the text is
        screen.blit(score_bg, (screen.get_width() // 2 - score_bg.get_width() // 2, 10))

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

        # the warning message
        if warning:
            font = pygame.font.SysFont('arial', 36)
            warning_text = font.render(warning, True, (255, 50, 50))
            # adding a glow effect when getting a warning
            warning_alpha = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 128 + 127
            warning_bg = pygame.Surface((warning_text.get_width() + 40, warning_text.get_height() + 20),
                                        pygame.SRCALPHA)
            warning_color = (0, 0, 0, int(warning_alpha))
            pygame.draw.rect(warning_bg, warning_color, warning_bg.get_rect(), border_radius=12)
            warning_bg.blit(warning_text, (20, 10))
            screen.blit(warning_bg, (screen.get_width() // 2 - warning_bg.get_width() // 2, 600))

        pygame.display.flip()


run_game(center_figure, figure_cards, ai)

# stop music before quitting
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
