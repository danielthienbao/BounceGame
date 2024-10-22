import pygame
import random

WIDTH, HEIGHT = 1200, 900

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 22, y - 22, 45, 45) 
        self.speed_x = 7 * random.choice((1, -1)) 
        self.speed_y = 7 * random.choice((1, -1))
        self.owner = None  # Track which player scored

    def move(self, paddle1_rect, paddle2_rect, goal_top, goal_bottom, screen_width):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ball bounce off the top and bottom edges of the screen (border)
        if self.rect.top <= 0 or self.rect.bottom >= 900:
            self.speed_y *= -1  # Reverse vertical direction

        # Ball bounce off the left and right edges, except in the goal area
        if self.rect.left <= 0:  # Left side
            if self.rect.top > goal_top and self.rect.bottom < goal_bottom:
                # The ball is within the goal area, so don't bounce
                self.owner = 'right'
            else:
                self.speed_x *= -1  # Bounce off the left border

        if self.rect.right >= screen_width:  # Right side
            if self.rect.top > goal_top and self.rect.bottom < goal_bottom:
                # The ball is within the goal area, so don't bounce
                self.owner = 'left'
            else:
                self.speed_x *= -1  # Bounce off the right border

        # Ball bounce off the paddles (adjust angle based on hit location)
        if self.rect.colliderect(paddle1_rect) or self.rect.colliderect(paddle2_rect):
            paddle_center = paddle1_rect.centery if self.rect.colliderect(paddle1_rect) else paddle2_rect.centery
            hit_diff = self.rect.centery - paddle_center
            angle = hit_diff / paddle1_rect.height  # Normalize the hit position
            self.speed_x *= -1  # Reverse horizontal direction
            self.speed_y += angle * 10  # Adjust Y speed based on where it hits the paddle

    def is_out_of_bounds(self):
        goal_top = HEIGHT // 2 - 100  # Top of the goal area
        goal_bottom = HEIGHT // 2 + 100  # Bottom of the goal area

        # Check if ball is on the left side (paddle1's side) and within goal bounds
        if self.rect.left <= 0 and goal_top <= self.rect.centery <= goal_bottom:
            self.owner = 'right'  # Right side scores
            return True

        # Check if ball is on the right side (paddle2's side) and within goal bounds
        elif self.rect.right >= WIDTH and goal_top <= self.rect.centery <= goal_bottom:
            self.owner = 'left'  # Left side scores
            return True

        return False

    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 0, 0), self.rect)
