import pygame
from parameters import *

class Character(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.image_right = img
        self.image_left = pygame.transform.flip(img, True, False)
        self.image_dash = img
        
        self.rect = self.image.get_rect()
        self.rect.left = SIZE*7
        self.rect.bottom = HEIGHT - 70

        # Variáveis do Movimento
        self.speedx = 0
        self.speedy = gravidade
        self.go_right = True
        self.go_left = True
        self.direction = 'right'
        self.jump = 0

        # Variáveis do personagem
        self.lifes = 1
        self.colors = []
        self.points = 0
        self.invencible = False

        # Variáveis do Shoot
        self.last_shoot = pygame.time.get_ticks()
        self.shoot_delay = 500
        
        # Variáveis do Dash
        self.FPS_dash = 150
        self.in_dash= False
        self.last_dash = pygame.time.get_ticks()
        self.dash_delay = 4000
        self.dash_duration = frame*3
     
    def update(self):
        self.speedy += 0 if self.speedy >= gravidade*4 else gravidade
        self.rect.y += self.speedy

        if self.rect.y < 0:
            self.rect.y == 0
            self.speedy = 0
        
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
            elapsed_ticks = now - self.last_shoot
            if elapsed_ticks > self.shoot_delay:
                self.last_shoot = now
                fireball = FireBall(img, self.rect.centerx, self.rect.centery, self.direction)
                groups['all_fireballs'].add(fireball)
                groups['all_sprites'].add(fireball)

    def dash(self):
        if "green" in self.colors:
            now = pygame.time.get_ticks()
            elapsed_ticks = now - self.last_dash
            if elapsed_ticks > self.dash_delay and not self.in_dash:
                self.last_dash = now
                if self.direction == 'right':
                    self.speedx = +70
                elif self.direction == 'left':
                    self.speedx = -70
                self.in_dash = True      

        
class Block(pygame.sprite.Sprite):
    def __init__(self, assets, posx, posy, nome):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.nome = nome

        self.image = assets[nome]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
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
    def __init__(self, assets, posx, posy, nome, moviment):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.nome = nome

        self.image = assets[nome]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = posx
        self.rect.top = posy + 20

        self.direction = moviment
        self.speed = moviment_enemy

    def update(self, player):
        if self.direction == "horizontal":
            self.rect.x += self.speed
        if self.direction == "vertical":
            self.rect.y += self.speed
            if self.rect.y < 0:
                self.rect.y = 0
                self.speed = -self.speed
            if self.rect.y > HEIGHT:
                self.rect.y = HEIGHT
                self.speed = -self.speed
        self.rect.x -= player.speedx 
    
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
