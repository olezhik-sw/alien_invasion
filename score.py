import pygame
import pygame.font

class Score():
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.font = pygame.font.SysFont(None, 45)
        self.scores = 0
        self.text_image = self.font.render(f"{self.scores}", True, (60, 70, 30))
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.right = self.screen_rect.right - 20
        self.text_image_rect.top = self.screen_rect.top + 20

    def show_score(self):
        self.screen.blit(self.text_image, self.text_image_rect)

    def update_score(self):
        self.scores += 10
        self.text_image = self.font.render(f"{self.scores}", True, (60, 70, 30))
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.right = self.screen_rect.right - 20
        self.text_image_rect.top = self.screen_rect.top + 20