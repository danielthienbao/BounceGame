import pygame
import sys
import random
from paddle import Paddle
from ball import Ball
from powerup import PowerUp, SlowPaddlePowerUp
from scoreboard import Scoreboard
from border import draw_border

pygame.init()

WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Two Player Bounce Game')
GOAL_TOP = HEIGHT // 2 - 200
GOAL_BOTTOM = HEIGHT // 2 + 200

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

# Center line boundary for paddles
CENTER_X = WIDTH // 2

# Create paddles (left and right)
paddle1 = Paddle(10, HEIGHT // 2)  # Adjust X based on width scaling
paddle2 = Paddle(WIDTH - 20, HEIGHT // 2)  # Adjust X based on width scaling

# Initialize balls
balls = [Ball(WIDTH // 2, HEIGHT // 2)]
scoreboard = Scoreboard()

# Power-up settings
power_ups = []
power_up_spawn_time = random.randint(1, 5) * 1000  # in milliseconds
last_power_up_spawn = pygame.time.get_ticks()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Reset paddle speed after slowdown effect
        if event.type == pygame.USEREVENT:
            paddle1.reset_speed()
            paddle2.reset_speed()
            paddle1.color = (255, 255, 255)  # Reset to original color
            paddle2.color = (255, 255, 255)  # Reset to original color

    # Move paddles (WASD for left, Arrow Keys for right)
    paddle1.move(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, True, WIDTH)

    paddle2.move(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, False, WIDTH)


    # Manage power-up spawning
    current_time = pygame.time.get_ticks()
    if current_time - last_power_up_spawn > power_up_spawn_time and len(power_ups) < 3:
        if random.choice([True, False]):
            power_ups.append(PowerUp())
        else:
            power_ups.append(SlowPaddlePowerUp())
        last_power_up_spawn = current_time
        power_up_spawn_time = random.randint(10, 20) * 1000  # Reset spawn time

    # Power-up collision with paddles
    for power_up in power_ups[:]:
        if power_up.rect.colliderect(paddle1.rect):
            power_up.activate(paddle1, balls)
            power_ups.remove(power_up)
        elif power_up.rect.colliderect(paddle2.rect):
            power_up.activate(paddle2, balls)
            power_ups.remove(power_up)

    # Move balls and handle collisions
    for ball in balls[:]:
        ball.move(paddle1.rect, paddle2.rect, GOAL_TOP, GOAL_BOTTOM, WIDTH)

        # Check if ball is out of bounds
        if ball.is_out_of_bounds():
            scoreboard.update(ball.owner)
            balls.remove(ball)

    # Respawn a new ball if none are present
    if not balls:
        balls.append(Ball(WIDTH // 2, HEIGHT // 2))

    # Check for game over
    if scoreboard.is_game_over():
        break

    # Game elements
    screen.fill(BLACK)
    draw_border(screen, WIDTH, HEIGHT)
    # Draw center line
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 8)


    # Draw paddles
    paddle1.draw(screen)
    paddle2.draw(screen)

    # Draw balls
    for ball in balls:
        ball.move(paddle1.rect, paddle2.rect, GOAL_TOP, GOAL_BOTTOM, WIDTH)  # Pass goal area and screen width
        ball.draw(screen)

    # Draw power-ups
    for power_up in power_ups:
        power_up.draw(screen)

    # Display score
    scoreboard.draw(screen, WIDTH)

    # Game over message
    if scoreboard.is_game_over():
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)
