import pygame

WIDTH = 900
HEIGHT = 600
gravidade = -10

class Personagem(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = 75
        self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        self.speedy = gravidade

class Block(pygame.sprite.Sprite):
    def __init__(self,img, posx, posy):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.image = img 
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.bottom = HEIGHT - 100
        self.pos_inicialy = posy
        self.speedx = 0
        self.speedy = gravidade

    def update(self,player):
        self.speedx= player.speedx
        self.speedy= player.speedy
        # Atualização da posição da nave
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.bottom < self.pos_inicialy:
            self.rect.bottom = self.pos_inicialy


    
