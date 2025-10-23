import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load("images\\alien.bmp").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.settings = ai_game.settings
        self.swap = False
        self.target = 0

        self.rect.x = self.rect.width / 2
        self.rect.y = self.screen_rect.top - self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
    
    def update(self):
        if self.rect.bottom - 30  >= self.screen_rect.bottom:
            self.settings.miss += 1
        if self.y <= self.screen_rect.bottom + self.rect.height:
            self.y += self.settings.alien_speed
            self.rect.y = self.y - self.rect.height
        else: 
            self.y = self.screen_rect.top
            
