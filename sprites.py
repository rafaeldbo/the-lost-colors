import pygame

WIDTH = 840
HEIGHT = 560
gravidade = 10

class Personagem(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = 75
        self.rect.bottom = HEIGHT - 70

        self.speedx = 0
        self.speedy = gravidade
        self.jump = True

    def update(self):
        self.speedy += gravidade
        self.rect.y += self.speedy

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
        self.speedx= - player.speedx
        # Atualização da posição da nave
        self.rect.x += self.speedx

class Monstrinho(pygame.sprite.Sprite):
    def __init__(self, img, posx, posy):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy

        self.speedx = 6

    def update(self, player):
        self.rect.x += self.speedx - player.speedx
