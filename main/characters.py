import pygame
from pygame.sprite import Sprite

from weapon import KnightWeapon, WizardWeapon, ElfWeapon


class Player(Sprite):

    def __init__(self, game_settings, screen, path):
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings
        self.speed = game_settings.player_speed
        self.path = path

        self.moving_right = False
        self.moving_left = False
        self.facing_right = True
        self.collision = False

        self.image = ''
        self.frame = 0
        self.idle_frames_r = []
        self.idle_frames_l = []
        self.run_frames_f = []
        self.run_frames_b = []
        self.load_frames()

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.center = 0
        self.mask = pygame.mask.from_surface(self.image)

        self.npc = True
        self.hp = 10
        self.damage = 0

    def load_frames(self):
        self.image = pygame.image.load(
            self.path + '_idle_f0.png')

        # Enlarges image by 6/4
        tmp_rect = self.image.get_rect()
        x_size = int((tmp_rect.width * 6) / 4)
        y_size = int((tmp_rect.height * 6) / 4)
        self.image = pygame.transform.scale(
            self.image, (x_size, y_size))

        # Stores each frame

        for i in range(4):
            # Loads and resizes for idle frames facing right
            temp_frame = pygame.image.load(
                self.path + '_idle_f' + str(i) + '.png')
            temp_frame = pygame.transform.scale(temp_frame, (x_size, y_size))
            self.idle_frames_r.append(temp_frame)

            # Loads and resizes for run frames facing right
            temp_frame = pygame.image.load(
                self.path + '_run_f' + str(i) + '.png')
            temp_frame = pygame.transform.scale(temp_frame, (x_size, y_size))
            self.run_frames_f.append(temp_frame)

        # Adds flipped frames for opposite direction
        for img in self.run_frames_f:
            self.run_frames_b.append(pygame.transform.flip(img, True, False))
        for img in self.idle_frames_r:
            self.idle_frames_l.append(pygame.transform.flip(img, True, False))

    def right(self):
        self.moving_right = self.facing_right = True
        self.moving_left = False

    def left(self):
        self.moving_right = self.facing_right = False
        self.moving_left = True

    def check_collision(self, sprite):
        if pygame.sprite.collide_mask(self, sprite):
            self.collision = True

    def update(self):
        super().update()

        if self.moving_right and not self.collision:
            self.image = self.run_frames_f[self.frame]

            if self.rect.centerx < self.screen_rect.width - 16:
                self.center += self.speed

        elif self.moving_left and not self.collision:
            self.image = self.run_frames_b[self.frame]

            if self.rect.centerx > 17:
                self.center -= self.speed

        elif self.facing_right is False:
            self.image = self.idle_frames_l[self.frame]

        else:
            self.image = self.idle_frames_r[self.frame]

        self.rect.centerx = self.center
        self.frame += 1
        self.frame %= self.game_settings.anicycle
        self.mask = pygame.mask.from_surface(self.image)
        self.collision = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Hero(Player):

    def __init__(self, game_settings, screen, hero):
        path = '../resources/' + hero + '/' + hero + '_m'
        super().__init__(game_settings, screen, path)

        self.rect.centerx = self.screen_rect.centerx / 3
        self.rect.bottom = self.screen_rect.bottom - game_settings.floor
        self.center = float(self.rect.centerx)

        self.npc = False
        self.weapon = ''

    def left(self):
        super().left()
        self.weapon.face_left()

    def right(self):
        super().right()
        self.weapon.face_right()

    def use_weapon(self):
        self.weapon.using = True

    def update(self):
        super().update()
        self.weapon.update(
            self.rect.centerx, self.rect.centery, self.facing_right)

    def blitme(self):
        self.weapon.blitme()
        super().blitme()


class Knight(Hero):

    def __init__(self, game_settings, screen, weapon):
        self.name = 'knight'
        super().__init__(game_settings, screen, self.name)
        self.hp = 20

        if weapon == 'bs' or weapon == 'bh' or weapon == 'ks':
            self.weapon = KnightWeapon(screen, self.rect, weapon)
        else:
            self.weapon = KnightWeapon(screen, self.rect)


class Wizard(Hero):

    def __init__(self, game_settings, screen, weapon):
        self.name = 'wizard'
        super().__init__(game_settings, screen, self.name)
        self.hp = 10

        if weapon == 'g' or weapon == 'r':
            self.weapon = WizardWeapon(screen, self.rect, weapon)
        else:
            self.weapon = WizardWeapon(screen, self.rect)

    def update(self):
        '''self.weapon.update(
            self.rect.centerx, self.rect.centery, self.facing_right)'''
        super().update()


class Elf(Hero):

    def __init__(self, game_settings, screen, weapon):
        self.name = 'elf'
        super().__init__(game_settings, screen, self.name)
        self.hp = 15

        if weapon == 'a' or weapon == 'b' or weapon == 'c' or weapon == 'd':
            self.weapon = ElfWeapon(screen, self.rect, weapon)
        else:
            self.weapon = ElfWeapon(screen, self.rect)

    def update(self):
        '''self.weapon.update(
            self.rect.centerx, self.rect.centery, self.facing_right)'''
        super().update()


class Mob(Player):

    def __init__(self, game_settings, screen, path):
        super().__init__(game_settings, screen, path)

        self.speed = game_settings.mob_speed

        self.rect.left = self.screen_rect.width
        self.rect.bottom = self.screen_rect.bottom - game_settings.floor
        self.center = float(self.rect.centerx)

        self.left()

        self.npc = True

    def check_collision(self, sprite):
        if pygame.sprite.collide_mask(self, sprite):
            self.collision = True
            sprite.hp -= self.damage
            print(sprite.name, 'hit')

    def update(self, player):
        super().update()

        if self.rect.centerx <= 17 and not self.collision:
            self.center -= self.speed


class BigDemon(Mob):

    def __init__(self, game_settings, screen):
        self.name = 'big demon'
        path = '../resources/' + 'demons/' + 'big_demon' + '/' + 'big_demon'
        super().__init__(game_settings, screen, path)

        self.hp = game_settings.bigDemonHP
        self.damage = self.bigDemonDamage


class Imp(Mob):

    def __init__(self, game_settings, screen):
        self.name = 'imp'
        path = '../resources/' + 'demons/' + 'imp' + '/' + 'imp'
        super().__init__(game_settings, screen, path)

        self.hp = game_settings.impHP
        self.damage = game_settings.impDamage

