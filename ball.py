import pygame
import random

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 15, y - 15, 30, 30)  # Ball size
        self.speed_x = 5 * random.choice((1, -1))
        self.speed_y = 5 * random.choice((1, -1))
        self.owner = None  # Track which player scored

    def move(self, paddle1_rect, paddle2_rect):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ball bounce top and bottom edges
        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.speed_y *= -1

        # Ball bounce paddles
        if self.rect.colliderect(paddle1_rect):
            self.speed_x *= -1
            self.owner = 'left'  # Mark the owner when colliding with left paddle
        elif self.rect.colliderect(paddle2_rect):
            self.speed_x *= -1
            self.owner = 'right'  # Mark the owner when colliding with right paddle

    def is_out_of_bounds(self):
        return self.rect.left <= 0 or self.rect.right >= 800

    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)
