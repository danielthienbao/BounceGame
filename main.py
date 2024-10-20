import pygame
import sys
import random
from paddle import Paddle
from ball import Ball
from powerup import PowerUp, SlowPaddlePowerUp
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
power_up_spawn_time = random.randint(1, 5) * 1000  # in milliseconds
last_power_up_spawn = pygame.time.get_ticks()

# To keep track of the last two paddles that touched the ball
last_touched_paddle = None
second_to_last_touched_paddle = None


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

    keys = pygame.key.get_pressed()
    paddle1.move(pygame.K_w, pygame.K_s)  # Move W/S
    paddle2.move(pygame.K_UP, pygame.K_DOWN)  # Move Up/Down arrows

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
            print("Paddle 1 hit a power-up!")
            power_up.activate(paddle1, balls)  # Only affect the paddle that activated the power-up
            power_ups.remove(power_up)   # Remove power-up after activation
        elif power_up.rect.colliderect(paddle2.rect):
            print("Paddle 2 hit a power-up!")
            power_up.activate(paddle2, balls)  # Only affect the paddle that activated the power-up
            power_ups.remove(power_up)   # Remove power-up after activation

    # Check for ball and power-up collision
    for ball in balls[:]:
        ball.move(paddle1.rect, paddle2.rect)

        # Track which paddles last touched the ball
        if ball.rect.colliderect(paddle1.rect):
            second_to_last_touched_paddle = last_touched_paddle
            last_touched_paddle = paddle1
        elif ball.rect.colliderect(paddle2.rect):
            second_to_last_touched_paddle = last_touched_paddle
            last_touched_paddle = paddle2

        # Check for ball and power-up collision
        for power_up in power_ups[:]:
            if ball.rect.colliderect(power_up.rect):
                print("Ball hit a power-up!")

                # Activate power-up effect (for SlowPaddlePowerUp, etc.)
                if isinstance(power_up, SlowPaddlePowerUp):
                    if second_to_last_touched_paddle:  # Ensure a paddle has been touched
                        power_up.activate(second_to_last_touched_paddle, balls)  # Pass the second-to-last paddle
                else:
                    power_up.activate(paddle2 if ball.rect.centerx < WIDTH // 2 else paddle1, balls)  # For normal power-ups
                
                # Remove power-up after activation
                power_ups.remove(power_up)

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
    paddle1.draw(screen)
    paddle2.draw(screen)

    # Draw the balls
    for ball in balls:
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
