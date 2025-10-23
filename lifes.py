import pygame

from pygame.sprite import Sprite

class Life(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load("images\\lifes.bmp").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.settings = ai_game.settings

        self.rect.x = 20
        self.rect.y = 20
    
    def life_draw(self):
        self.screen.blit(self.image, self.rect)