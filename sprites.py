from turtle import right
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
        self.rect.left = 140
        self.rect.bottom = HEIGHT - 70

        self.speedx = 0
        self.speedy = gravidade

        self.jump = True
        self.go_right = True
        self.go_left = True
        self.direction = 'right'

        self.lifes = 1

        # Só será possível atirar uma vez a cada 500 milissegundos
        self.fireballs = False
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500
        
    def update(self):
        self.speedy += 0 if self.speedy >= 30 else gravidade
        self.rect.y += self.speedy
        
        if self.speedx > 0:
            self.image = self.image_right
            self.direction = 'right'
        elif self.speedx < 0:
            self.image = self.image_left
            self.direction= 'left'

    def shoot (self, img, all_bolinhas):
        if self.fireballs:
            # Verifica se pode atirar
            now = pygame.time.get_ticks()
            # Verifica quantos ticks se passaram desde o último tiro.
            elapsed_ticks = now - self.last_shot

            # Se já pode atirar novamente...
            if elapsed_ticks > self.shoot_ticks:
                # Marca o tick da nova imagem.
                self.last_shot = now
                nova_bolinha = FireBolinha(img, self.rect.centerx, self.rect.centery, self.direction)
                all_bolinhas.add(nova_bolinha)

class Block(pygame.sprite.Sprite):
    def __init__(self,img, posx, posy):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img 
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy

        self.speedx = 0

    def update(self,player):
        self.speedx = -player.speedx
        self.rect.x += self.speedx

        player.go_right = True
        player.go_left = True

class Enemy(pygame.sprite.Sprite):
    def __init__(self, img, posx, posy):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy + 20

        self.speedx = 6

    def update(self, player):
        self.rect.x += self.speedx - player.speedx

class FireBolinha(pygame.sprite.Sprite):
    def __init__(self, img, posx, posy, direction):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.rect = img.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy

        if direction == 'right':
            self.speedx = 15
            self.image = img
        elif direction == 'left':
            self.speedx = -15
            self.image = pygame.transform.flip(img, True, False)

    def update(self, player):
        self.rect.x += self.speedx - player.speedx

class Diamonds(pygame.sprite.Sprite):
    def __init__(self, img, posx, posy):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy

        self.speedx = 0

    def update(self, player):
        self.speedx = -player.speedx
        self.rect.x += self.speedx