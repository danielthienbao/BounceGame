import pygame
import random
from ball import Ball

class PowerUp:
    def __init__(self):
        self.radius = 25
        self.rect = pygame.Rect(random.randint(100, 700), random.randint(100, 500), self.radius * 2, self.radius * 2)

    def activate(self, paddle, balls):
        # Default power-up spawns two extra balls
        for _ in range(3):  # Change to 3 balls
            new_ball = Ball(400, 300)
            balls.append(new_ball)

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), self.rect.center, self.radius)


class SlowPaddlePowerUp(PowerUp):
    def __init__(self):
        super().__init__()
        self.color = (173, 216, 230)  # Light blue (RGB values)
        self.original_color = (255, 255, 255)  # Original color (white or whatever your paddle's default is)

    def activate(self, paddle, balls):
        # Change paddle color to blue
        paddle.color = self.color
        paddle.slow_down(50, 10000)  # Slow down by 50% for 10 seconds

        # Set an event to reset the paddle's color after 10 seconds
        pygame.time.set_timer(pygame.USEREVENT, 10000)  # 10 seconds

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
