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

        # Ball bounce off the paddles (adjust angle based on hit location)
        if self.rect.colliderect(paddle1_rect) or self.rect.colliderect(paddle2_rect):
            paddle_center = paddle1_rect.centery if self.rect.colliderect(paddle1_rect) else paddle2_rect.centery
            hit_diff = self.rect.centery - paddle_center
            angle = hit_diff / paddle1_rect.height  # Normalize the hit position
            self.speed_x *= -1
            self.speed_y += angle * 10  # Adjust Y speed based on where it hits the paddle

    def is_out_of_bounds(self):
        if self.rect.left <= 0:
            self.owner = 'right'  # Right side scores
            return True
        elif self.rect.right >= 800:
            self.owner = 'left'   # Left side scores
            return True
        return False

    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)
