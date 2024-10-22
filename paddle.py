import pygame

class Paddle:
    def __init__(self, x, y, is_left=True):
        self.x = x
        self.y = y
        self.radius = 45
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.original_speed = 15
        self.speed = self.original_speed
        self.is_left = is_left  # Add flag to check which side the paddle is on

    def slow_down(self, percentage, duration):
        self.speed = self.original_speed * (percentage / 100)
        pygame.time.set_timer(pygame.USEREVENT, duration)

    def move(self, up_key, down_key, left_key, right_key, is_left_paddle, screen_width):
        keys = pygame.key.get_pressed()

        # Vertical movement (up and down)
        if keys[up_key] and self.rect.top > 0:  # Ensure it doesn't go off the top
            self.rect.y -= self.speed
        if keys[down_key] and self.rect.bottom < 900:  # Ensure it doesn't go off the bottom (new height is 900)
            self.rect.y += self.speed

        # Horizontal movement (left and right) with boundary check based on paddle position
        if is_left_paddle:
            if keys[left_key] and self.rect.left > 0:  # Left paddle shouldn't go beyond the left edge
                self.rect.x -= self.speed
            if keys[right_key] and self.rect.right < screen_width // 2:  # Left paddle can't cross the center line
                self.rect.x += self.speed
        else:
            if keys[left_key] and self.rect.left > screen_width // 2:  # Right paddle can't cross the center line
                self.rect.x -= self.speed
            if keys[right_key] and self.rect.right < screen_width:  # Right paddle shouldn't go beyond the right edge
                self.rect.x += self.speed


    def reset_speed(self):
        self.speed = self.original_speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.rect.center, self.radius)
