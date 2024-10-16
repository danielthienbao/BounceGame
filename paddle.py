import pygame

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y - 50, 10, 100)  # Paddle size and position

    def move(self, up_key, down_key):
        keys = pygame.key.get_pressed()
        if keys[up_key] and self.rect.top > 0:
            self.rect.y -= 8
        if keys[down_key] and self.rect.bottom < 600:
            self.rect.y += 8

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
