import pygame
import random
from ball import Ball
class PowerUp:
    def __init__(self):
        self.radius = 15
        self.rect = pygame.Rect(random.randint(100, 700), random.randint(100, 500), self.radius * 2, self.radius * 2)

    def activate(self, balls):
        
        for _ in range(2):
            new_ball = Ball(400, 300)
            balls.append(new_ball)

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), self.rect.center, self.radius)
