import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spelling Game")

# Load static background image
try:
    background_image = pygame.image.load('game/ocean.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except:
    print("Error loading image. Ensure 'ocean.png' exists in the game folder.")
    background_image = pygame.Surface((WIDTH, HEIGHT))
    background_image.fill((0, 0, 255))  # Default to blue background if image not loaded

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (219, 55, 55)
GREEN = (48, 199, 108)
BLUE = (55, 101, 219)
GRAY = (115, 131, 133)
DARKGRAY = (57, 63, 64)
LIGHTBLUE = (50, 193, 207)

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Game settings
FPS = 165
scroll_speed = 10
original_word_list = ["word", "game", "code", "beat", "text"]
used_words = []
max_words = 5
circle_radius = 40  # Radius of the circular hit zone
trigger_line_x = 130  # X position for the trigger line

# Game variables
target_word = random.choice(original_word_list)
target_index = 0
letters_correct = 0
total_letters_attempted = 0
words_correct = 0
words_attempted = 0  # New variable to track total words attempted
missed_letters = []
letter_status = [GRAY] * len(target_word)  # Status for each letter (GRAY = pending, GREEN = correct, RED = incorrect)
scroll_x = WIDTH
timer = 0
game_started = False
game_paused = False
game_over = False
current_row = random.choice([0, 1])  # Randomized row

# Functions
def reset_game():
    global target_word, target_index, scroll_x, letters_correct, total_letters_attempted, missed_letters, letter_status, game_over, words_correct, words_attempted, current_row

    # Check if the max word limit is reached
    if words_attempted >= max_words:
        game_over = True
        return  # Stop further resetting if game is over

    # Continue game reset if limit not reached
    available_words = list(set(original_word_list) - set(used_words))
    if not available_words:  # Reset used words if all words are used
        available_words = original_word_list.copy()
        used_words.clear()

    target_word = random.choice(available_words)
    used_words.append(target_word)
    target_index = 0
    scroll_x = WIDTH
    missed_letters.clear()
    letter_status = [GRAY] * len(target_word)  # Reset letter colors to gray
    current_row = random.choice([0, 1])  # Randomize the row for the first letter

def draw_text(text, font, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

def draw_button(text, x, y, width, height, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    draw_text(text, small_font, WHITE, x + 20, y + 10)
    return False

def draw_indicator_boxes(z_active, x_active):
    # Draw the "Z" box
    z_color = DARKGRAY if z_active else GRAY
    pygame.draw.rect(screen, z_color, (50, HEIGHT // 2 - 60, 60, 60), border_radius=10)
    draw_text("Z", small_font, BLACK, 65, HEIGHT // 2 - 50)

    # Draw the "X" box
    x_color = DARKGRAY if x_active else GRAY
    pygame.draw.rect(screen, x_color, (50, HEIGHT // 2 + 20, 60, 60), border_radius=10)
    draw_text("X", small_font, BLACK, 65, HEIGHT // 2 + 30)


# Main game loop
clock = pygame.time.Clock()
running = True
game_over = False
z_pressed = False
x_pressed = False

while running:
    # Display static background
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_over:
                    running = False  # Close the game on ESC if game is over
                else:
                    game_paused = not game_paused  # Toggle pause on ESC during gameplay
            if event.key == pygame.K_z and game_started and not game_paused:
                z_pressed = True
                z_hold_start_time = pygame.time.get_ticks()
            elif event.key == pygame.K_x and game_started and not game_paused:
                x_pressed = True
                x_hold_start_time = pygame.time.get_ticks()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                z_pressed = False
                z_hold_start_time = None
            elif event.key == pygame.K_x:
                x_pressed = False
                x_hold_start_time = None

    # Draw Start button if the game hasn't started yet
    if not game_started:
        if draw_button("Start", WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50, BLUE, GREEN):
            game_started = True
            reset_game()
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Display game over screen without words/circles
    if game_over:
        accuracy = int((letters_correct / total_letters_attempted) * 100) if total_letters_attempted > 0 else 0
        draw_text(f"Words Correct: {words_correct} / {max_words}", font, BLACK, WIDTH // 2 - 150, HEIGHT // 2 - 100)
        draw_text(f"Accuracy: {accuracy}%", font, BLACK, WIDTH // 2 - 100, HEIGHT // 2)

        # Draw Play Again button
        if draw_button("Play Again", WIDTH // 2 - 60, HEIGHT // 2 + 80, 120, 50, BLUE, GREEN):
            # Reset all necessary variables for a new game
            words_correct = 0
            words_attempted = 0
            total_letters_attempted = 0
            letters_correct = 0
            game_over = False
            reset_game()
            game_started = True

        draw_text("Press ESC to Exit", small_font, BLACK, WIDTH // 2 - 80, HEIGHT // 2 + 150)
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Check if the game is paused
    if game_paused:
        draw_text("Paused", font, BLACK, WIDTH // 2 - 70, HEIGHT // 2 - 30)
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Game mechanics only run when game is active
    if not game_over:
        # Draw the trigger line
        pygame.draw.line(screen, RED, (trigger_line_x, 0), (trigger_line_x, HEIGHT), 2)

        # Draw indicator boxes
        draw_indicator_boxes(z_pressed, x_pressed)

        # Draw the target word at the top with letter colors
        for i, letter in enumerate(target_word):
            color = letter_status[i]
            draw_text(letter.upper(), font, color, WIDTH // 2 - 100 + i * 50, 50)

        # Handle letter scrolling and hit detection
        scroll_x -= scroll_speed
        current_letter = target_word[target_index] if target_index < len(target_word) else ""

        # Draw circle and letter based on `current_row`
        row_y = HEIGHT // 2 - 40 if current_row == 0 else HEIGHT // 2 + 40
        pygame.draw.circle(screen, LIGHTBLUE, (scroll_x, row_y), circle_radius)
        pygame.draw.circle(screen, BLACK, (scroll_x, row_y), circle_radius, 3)  # Black outline
        draw_text(current_letter.upper(), font, BLACK, scroll_x - 20, row_y - 30)

        # Release "Z" or "X" press if held longer than 1 second
        if z_pressed and z_hold_start_time and pygame.time.get_ticks() - z_hold_start_time > 1000:
            z_pressed = False
            z_hold_start_time = None
        if x_pressed and x_hold_start_time and pygame.time.get_ticks() - x_hold_start_time > 1000:
            x_pressed = False
            x_hold_start_time = None

        # Check if the letter reaches the trigger line and check for user input
        if scroll_x <= trigger_line_x:
            if (current_row == 0 and z_pressed) or (current_row == 1 and x_pressed):
                letter_status[target_index] = GREEN
                letters_correct += 1
            else:
                letter_status[target_index] = RED
                missed_letters.append(current_letter)
            target_index += 1
            scroll_x = WIDTH
            total_letters_attempted += 1

            # Check if the word is fully completed
            if target_index >= len(target_word):
                words_attempted += 1  # Increment total words attempted
                if all(color == GREEN for color in letter_status):  # Only increment if all letters are correct
                    words_correct += 1

                if words_attempted >= max_words:
                    game_over = True
                else:
                    reset_game()  # Move to the next word or end the game

    # Refresh the screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
