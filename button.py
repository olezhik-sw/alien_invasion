import pygame
from pygame.sprite import Sprite
import pygame.font

class Button(Sprite):
    def __init__(self, text, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.font = pygame.font.SysFont(None, 60)
        self.text_image = self.font.render(text, True, (250, 250, 250))
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.screen_rect.center
        self.bg_surface = pygame.Surface((self.text_image_rect.width + 80, self.text_image_rect.height + 30), pygame.SRCALPHA)
        self.bg_surface_rect = self.bg_surface.get_rect()
        self.bg_surface_rect.center = self.text_image_rect.center
        pygame.draw.rect(
            self.bg_surface,
            (217, 217, 217, 55),
            self.bg_surface.get_rect(),
            border_radius=15
        )
    
    def show_button(self):
        self.screen.blit( self.bg_surface, self.bg_surface_rect)
        self.screen.blit(self.text_image, self.text_image_rect)
