import pygame

class Ship():
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load("images\\ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (180, 180))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.bottom += 25
        self.moved_right = False
        self.moved_left = False
        self.settings = ai_game.settings
        self.x = float(self.rect.x)
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        if self.moved_left and self.rect.left > - 15:
            self.x -= self.settings.ship_speed
        elif self.moved_right and self.rect.right < self.screen_rect.right + 15:
            self.x += self.settings.ship_speed
        self.rect.x = self.x

    def reset(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.bottom += 25
        self.moved_right = False
        self.moved_left = False
        self.x = float(self.rect.x)