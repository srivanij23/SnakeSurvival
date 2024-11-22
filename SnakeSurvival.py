import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake SURVIVAL")

# Light and Dark Mode Themes
LIGHT_MODE = {
    "background": (240, 240, 240),  # Light Grey
    "snake": (50, 150, 50),         # Dark Green
    "food": (200, 50, 50),          # Dark Red
    "text": (60, 60, 60),           # Dark Grey
    "mode_icon": "🌞"               # Sun emoji for light mode
}

DARK_MODE = {
    "background": (20, 20, 20),     # Very Dark Grey
    "snake": (0, 255, 0),           # Bright Green
    "food": (255, 0, 0),            # Bright Red
    "text": (255, 255, 255),        # White
    "mode_icon": "🌜"               # Moon emoji for dark mode
}

# Game settings
snake_block = 20
initial_speed = 10
is_dark_mode = True
current_theme = DARK_MODE

# Initialize clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 35)
mode_font = pygame.font.SysFont('segoe ui emoji', 30)  # Font that supports emojis

class ThemeToggleButton:
    def __init__(self):
        self.width = 50
        self.height = 30
        self.x = width - 60
        self.y = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self):
        # Draw button background
        pygame.draw.rect(window, current_theme["text"], self.rect, 2, 10)
        
        # Draw mode icon
        mode_text = mode_font.render(current_theme["mode_icon"], True, current_theme["text"])
        window.blit(mode_text, (self.x + 10, self.y))
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

theme_button = ThemeToggleButton()

def toggle_theme():
    global current_theme, is_dark_mode
    is_dark_mode = not is_dark_mode
    current_theme = DARK_MODE if is_dark_mode else LIGHT_MODE

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(window, current_theme["snake"], 
                        [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace=0):
    mesg = font.render(msg, True, color)
    window.blit(mesg, [width/6, height/3 + y_displace])

def show_score(score):
    score_text = font.render("Score: " + str(score), True, current_theme["text"])
    window.blit(score_text, [10, 10])

def calculate_speed(score):
    return min(initial_speed + (score * 0.5), 25)

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    score = 0
    current_speed = initial_speed

    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    while not game_over:

        while game_close:
            window.fill(current_theme["background"])
            message(f"You Lost! Score: {score}", current_theme["text"])
            message("Press Q-Quit or C-Play Again", current_theme["text"], 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if theme_button.is_clicked(event.pos):
                    toggle_theme()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change <= 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change >= 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change <= 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change >= 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
            
        x1 += x1_change
        y1 += y1_change
        window.fill(current_theme["background"])
        
        # Draw food
        pygame.draw.rect(window, current_theme["food"], 
                        [foodx, foody, snake_block, snake_block])
        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        show_score(score)
        theme_button.draw()

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            score += 1
            current_speed = calculate_speed(score)

        clock.tick(current_speed)

    pygame.quit()
    quit()

gameLoop()
