import pygame
import sys
import random
from paddle import Paddle
from ball import Ball
from powerup import PowerUp
from scoreboard import Scoreboard

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Two Player Bounce Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

paddle1 = Paddle(10, HEIGHT // 2)
paddle2 = Paddle(WIDTH - 20, HEIGHT // 2)

# Initialize balls
balls = [Ball(WIDTH // 2, HEIGHT // 2)]
scoreboard = Scoreboard()

# Power-up settings
power_ups = []
power_up_spawn_time = random.randint(15, 30) * 1000  # in milliseconds
last_power_up_spawn = pygame.time.get_ticks()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    paddle1.move(pygame.K_w, pygame.K_s)  # Move W/S
    paddle2.move(pygame.K_UP, pygame.K_DOWN)  # Move Up/Down arrows

    # Manage powerup spawning
    current_time = pygame.time.get_ticks()
    if current_time - last_power_up_spawn > power_up_spawn_time:
        power_ups.append(PowerUp())
        last_power_up_spawn = current_time
        power_up_spawn_time = random.randint(15, 25) * 1000  # Reset spawn time

    # powerup collision with paddles
    for power_up in power_ups[:]:
        if power_up.rect.colliderect(paddle1.rect) or power_up.rect.colliderect(paddle2.rect):
            power_up.activate(balls)
            power_ups.remove(power_up)

    # powerup collision with balls
    for ball in balls[:]:
        for power_up in power_ups[:]:
            if power_up.rect.colliderect(ball.rect):
                power_up.activate(balls)
                power_ups.remove(power_up)

    # Move the balls and check collisions
    for ball in balls[:]:
        ball.move(paddle1.rect, paddle2.rect)
        if ball.is_out_of_bounds():
            scoreboard.update(ball.owner)
            balls.remove(ball)

    # Respawn a new ball if none are present
    if not balls:
        balls.append(Ball(WIDTH // 2, HEIGHT // 2))

    # Check for game over
    if scoreboard.is_game_over():
        break

    # game elements
    screen.fill(BLACK)
    paddle1.draw(screen)
    paddle2.draw(screen)

    # Draw the balls
    for ball in balls:
        ball.draw(screen)

    # Draw powerups
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
