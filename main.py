import sys
import pygame

from ship import Ship
from settings import Settings
from bullet import  Bullet
from alien import Alien
from score import Score
from lifes import Life
from button import Button
from random import randint, choice

class AlienInvasion():
    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width
        self.bg_color = self.settings.bg_color
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.score = Score(self)
        self.lifes = pygame.sprite.Group()
        self.button = pygame.sprite.Group()
        self.start_button = Button("Play", self)
        self.restart_button = Button("Restart", self)

        self._create_lifes()
        self._create_fleet()
        pygame.display.set_caption("AlienInvasion")

    def run_game(self):
        clock = pygame.time.Clock()
        while True:
            self._check_events()

            self.ship.update()
            self.bullets.update()
            self._update_bullets()

            self._update_screen()
            clock.tick(144)

    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._click_start_button(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _update_screen(self):
        if not self.lifes:
            self.settings.end_screen = True
            bg_surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
            bg_surface_rect = bg_surface.get_rect()
            bg_surface.fill((61, 61, 41, 200))
            self.screen.blit(bg_surface, bg_surface_rect)
            result = Button(f"Your score: {self.score.scores}", self)
            result.bg_surface_rect.y -= 90
            result.text_image_rect.y -= 90
            result.show_button()
            self.restart_button.show_button()
        else:
            self.screen.fill(self.bg_color)
            self.ship.blitme()
            self.aliens.draw(self.screen)
            self.score.show_score()
            for life in self.lifes:
                life.life_draw()
            if self.settings.start_screen:
                bg_surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
                bg_surface_rect = bg_surface.get_rect()
                bg_surface.fill((61, 61, 41, 200))
                self.screen.blit(bg_surface, bg_surface_rect)
                self.start_button.show_button()
            else: 
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
                for alien in self.aliens:
                    if 4 == choice(range(800)):
                        self._swap_pos()
                    if alien.swap:
                        self._swap(alien)
                    alien.update()
                if self.settings.miss > 0:
                    self._update_lifes()
                self._leveling()
        pygame.display.flip()

    def _check_keydown_events(self, event):
        if not self.settings.start_screen:
            if event.key == pygame.K_RIGHT:
                self.ship.moved_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moved_left = True
            # elif event.key == pygame.K_f:
            #     self._toggle_fullscreen()
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()
            elif event.key == pygame.K_r:
                self._create_lifes()
        elif event.key == pygame.K_SPACE:
                self.settings.start_screen = False
                self.bg_color = self.settings.bg_color
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moved_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moved_left = False
    
    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
        if collisions and not self.settings.end_screen:
            for bullet, aliens in collisions.items():
                aliens[0].y = self.screen.get_rect().top - aliens[0].rect.height
                aliens[0].rect.y = aliens[0].y
                self.score.update_score()
        if not self.aliens:
            pass
            #self.bullets.empty()
            #self._create_fleet()
        # else: 
        #     print(len(self.aliens))

    def _create_fleet(self):
        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (alien_width)
        number_aliens_x = available_space_x // (alien_width * 2)
        for alien_number in range(number_aliens_x + 1):
            self._create_alien(alien_number)

    def _create_alien(self, alien_number):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        self.aliens.add(alien)

    def _swap_pos(self):
        aliens = sorted(self.aliens, key=lambda a: (a.rect.y, a.rect.x))
        if len(aliens) < 1:
            return
        first = choice(aliens)
        same_row = [a for a in aliens if abs(a.rect.y - first.rect.y) < first.rect.height // 2]
        if len(same_row) == 1:
            screen_width = self.screen.get_width()
            width = first.rect.width
            direction = choice([-1, 1])
            step = width * choice([1, 2])
            new_x = first.rect.x + direction * step
            if new_x < width:
                new_x = first.rect.x + step
            elif new_x + width > screen_width:
                new_x = first.rect.x - step
            first.swap = True
            first.target = new_x
            return
        same_row.sort(key=lambda a: a.rect.x)
        idx = same_row.index(first)
        if idx == 0:
            neighbor = same_row[1]
        elif idx == len(same_row) - 1:
            neighbor = same_row[-2]
        else:
            neighbor = choice([same_row[idx - 1], same_row[idx + 1]])
        if not first.swap and not neighbor.swap:
            first.swap = neighbor.swap = True
            first.target = neighbor.rect.x
            neighbor.target = first.rect.x

    def _swap(self, alien):
        if alien.x < alien.target and alien.swap:
            alien.x += self.settings.alien_swap_speed
            alien.rect.x = alien.x
        elif alien.x > alien.target and alien.swap:
            alien.x -= self.settings.alien_swap_speed
            alien.rect.x = alien.x
        elif alien.x == alien.target and alien.swap:
            alien.swap = False

    def _create_lifes(self):
        for count in range(self.settings.count_lifes):
            life = Life(self)
            life.rect.x = (life.rect.width * (count)) + 20
            self.lifes.add(life)

    def _update_lifes(self):
        for x in range(self.settings.miss):
            if self.lifes:
                last = list(self.lifes)[-1]
                self.lifes.remove(last)
                self.settings.miss -= 1

    def _click_start_button(self, mouse_pos):
        if self.start_button.bg_surface_rect.collidepoint(mouse_pos) and self.lifes:
            self.settings.start_screen = False
        elif self.restart_button.bg_surface_rect.collidepoint(mouse_pos):
            self.reset_game()

    def reset_game(self):
        if self.aliens:
            for item in self.aliens:
                self.aliens.remove(item)
            self._create_fleet()
        else: 
            self._create_fleet()
        if self.lifes:
            for item in self.lifes:
                self.lifes.remove(item)
            self._create_lifes()
        else: 
            self._create_lifes()
        self.ship.reset()
        self.score.scores = 0
        self.score.text_image = self.score.font.render(f"{self.score.scores}", True, (60, 70, 30))
        self.settings.alien_speed = 1
        self.settings.ship_speed = 8
        self.settings.bullet_speed = 5
        self.settings.end_screen = False

    def _leveling(self):
        for lvl in range(1,11):
            if self.score.scores == lvl * 100:
                self.settings.alien_speed += lvl / 300
                self.settings.ship_speed += lvl / 60
                self.settings.bullet_speed += lvl / 90

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()