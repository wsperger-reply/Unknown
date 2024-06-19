import pygame
import sys
import time
import random

# Initialize pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Snake block size
BLOCK_SIZE = 20

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

# Function to display messages on screen
def display_message(message, color, font_size, position):
    font = pygame.font.SysFont(None, font_size)
    text = font.render(message, True, color)
    screen.blit(text, position)

# Function to draw the snake
def draw_snake(snake_body):
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

# Function to generate food
def generate_food():
    return [random.randrange(1, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
            random.randrange(1, (SCREEN_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]

# Function to run the game
def game():
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_position = generate_food()
    direction = 'RIGHT'
    change_to = direction
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_d and direction != 'LEFT':
                    change_to = 'RIGHT'
                elif event.key == pygame.K_w and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_s and direction != 'UP':
                    change_to = 'DOWN'

        # Validate direction
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'

        # Move the snake
        if direction == 'RIGHT':
            snake_position[0] += BLOCK_SIZE
        if direction == 'LEFT':
            snake_position[0] -= BLOCK_SIZE
        if direction == 'UP':
            snake_position[1] -= BLOCK_SIZE
        if direction == 'DOWN':
            snake_position[1] += BLOCK_SIZE

        # Snake body mechanism
        snake_body.insert(0, list(snake_position))
        if snake_position == food_position:
            score += 1
            food_position = generate_food()
        else:
            snake_body.pop()

        # Draw everything
        screen.fill(BLACK)
        draw_snake(snake_body)
        pygame.draw.rect(screen, RED, [food_position[0], food_position[1], BLOCK_SIZE, BLOCK_SIZE])

        # Display score
        display_message(f"Score: {score}", WHITE, 24, [10, 10])

        # Game over conditions
        if (snake_position[0] < 0 or snake_position[0] >= SCREEN_WIDTH or
                snake_position[1] < 0 or snake_position[1] >= SCREEN_HEIGHT):
            display_message("Game Over!", RED, 50, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3])
            pygame.display.update()
            time.sleep(2)
            return

        if snake_position in snake_body[1:]:
            display_message("Game Over!", RED, 50, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3])
            pygame.display.update()
            time.sleep(2)
            return

        pygame.display.update()
        clock.tick(10)

# Start the game loop
while True:
    game()
    time.sleep(5)  # Restart the game after 5 seconds
