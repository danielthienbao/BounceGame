import pygame

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 50
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.original_speed = 10
        self.speed = self.original_speed

    def slow_down(self, percentage, duration):
        self.speed = self.original_speed * (percentage / 100)
        pygame.time.set_timer(pygame.USEREVENT, duration)

    def move(self, up_key, down_key):
        keys = pygame.key.get_pressed()
        if keys[up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down_key] and self.rect.bottom < 600:
            self.rect.y += self.speed

    def reset_speed(self):
        self.speed = self.original_speed

    def draw(self, screen):
        # Draw a normal circle for the paddles
        pygame.draw.circle(screen, (255, 255, 255), self.rect.center, self.radius)