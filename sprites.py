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

        self.lifes = 1
        
    def update(self):
        self.speedy += 0 if self.speedy >= 30 else gravidade
        self.rect.y += self.speedy
        
        if self.speedx > 0:
            self.image = self.image_right
        elif self.speedx < 0:
            self.image = self.image_left

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
