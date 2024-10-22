import pygame

WHITE = (255, 255, 255)  # Define color constant for white

# Constants for goal area, assuming width and height are passed from main.py
def draw_border(screen, width, height):
    goal_top = height // 2 - 100
    goal_bottom = height // 2 + 100

    # Top border
    pygame.draw.line(screen, WHITE, (0, 0), (width, 0), 5)  # Full top line
    # Bottom border
    pygame.draw.line(screen, WHITE, (0, height), (width, height), 5)  # Full bottom line
    
    # Left border (above the goal)
    pygame.draw.line(screen, WHITE, (0, 0), (0, goal_top), 5)  # From top to start of goal
    # Left border (below the goal)
    pygame.draw.line(screen, WHITE, (0, goal_bottom), (0, height), 5)  # From end of goal to bottom
    
    # Right border (above the goal)
    pygame.draw.line(screen, WHITE, (width, 0), (width, goal_top), 5)  # From top to start of goal
    # Right border (below the goal)
    pygame.draw.line(screen, WHITE, (width, goal_bottom), (width, height), 5)  # From end of goal to bottom
