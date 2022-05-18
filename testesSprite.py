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
        self.energy = 0
        self.j = False

    def jump(self):
        self.energy = 70 

    def update(self):
        self.rect.y -= self.energy
        self.energy -= 5

class Block(pygame.sprite.Sprite):
    def __init__(self,img, posx, posy):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.image = img 
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.bottom = posy
        self.speedx = 0

    def update(self):
        # Atualização da posição da nave
        self.rect.x += self.speedx