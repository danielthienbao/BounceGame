import pygame

class Scoreboard:
    def __init__(self):
        self.score1 = 0
        self.score2 = 0

    def update(self, owner):
        if owner == 'left':
            self.score1 += 1
        else:
            self.score2 += 1

    def is_game_over(self):
        return self.score1 >= 10 or self.score2 >= 10

    def draw(self, screen, width):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"{self.score1} : {self.score2}", True, (255, 255, 255))
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))
