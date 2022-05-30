import pygame
from parameters import *

class Character(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.image_right = img
        self.image_left = pygame.transform.flip(img, True, False)
        
        self.rect = self.image.get_rect()
        self.rect.left = SIZE*7
        self.rect.bottom = HEIGHT - 70

        self.speedx = 0
        self.speedy = gravidade

        self.jump = True
        self.go_right = True
        self.go_left = True
        self.direction = 'right'

        self.lifes = 1
        self.colors = []
        self.points = 0

        # Só será possível atirar uma vez a cada 500 milissegundos
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500
        
    def update(self):
        self.speedy += 0 if self.speedy >= gravidade*4 else gravidade
        self.rect.y += self.speedy
        
        if self.speedx > 0:
            self.direction = 'right'
        elif self.speedx < 0:
            self.direction= 'left'

        if self.direction == 'right':
            self.image = self.image_right
        elif self.direction == 'left':
            self.image = self.image_left

    def update_color(self, assets):
        self.image_right = assets['personagem']
        self.image_left = pygame.transform.flip(assets['personagem'], True, False)

    def shoot (self, img, groups):
        if "red" in self.colors:
            now = pygame.time.get_ticks()
            elapsed_ticks = now - self.last_shot
            if elapsed_ticks > self.shoot_ticks:
                self.last_shot = now
                fireball = FireBall(img, self.rect.centerx, self.rect.centery, self.direction)
                groups['all_fireballs'].add(fireball)
                groups['all_sprites'].add(fireball)

class Block(pygame.sprite.Sprite):
    def __init__(self, assets, posx, posy, nome):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.nome = nome

        self.image = assets[nome]
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy

        self.speedx = 0

    def update(self,player):
        self.speedx = -player.speedx
        self.rect.x += self.speedx

        player.go_right = True
        player.go_left = True
    
    def update_color(self, assets):
        self.image = assets[self.nome]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, assets, posx, posy, nome):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.nome = nome

        self.image = assets[nome]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = posx
        self.rect.top = posy + 20

        self.speedx = moviment_enemy_x

    def update(self, player):
        self.rect.x += self.speedx - player.speedx
    
    def update_color(self, assets):
        self.image = assets[self.nome]

class FireBall(pygame.sprite.Sprite):
    def __init__(self, img, posx, posy, direction):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.rect = img.get_rect()
        self.mask = pygame.mask.from_surface(img)
        self.rect.centerx = posx
        self.rect.centery = posy

        if direction == 'right':
            self.speedx = moviment_fireball_x
            self.image = img
        elif direction == 'left':
            self.speedx = -moviment_fireball_x
            self.image = pygame.transform.flip(img, True, False)

    def update(self, player):
        self.rect.x += self.speedx -player.speedx

class Collectable(pygame.sprite.Sprite):
    def __init__(self, assets, posx, posy, nome, **kargs):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.nome = nome

        self.color = kargs.get('prism')
        if self.color != None:
            img = pygame.image.load(f'assets/img/{nome}.png')
            self.image = pygame.transform.scale(img, (50, 50))
            posx += 10
            posy += 10
        else:
            self.image = assets[nome]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = posx
        self.rect.top = posy

        self.speedx = 0

    def update(self, player):
        self.speedx = -player.speedx
        self.rect.x += self.speedx
    
    def update_color(self, assets):
        if self.color == None:
            self.image = assets[self.nome]