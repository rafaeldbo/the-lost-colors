import pygame
from parameters import *
assets= {}

background_img = pygame.image.load('assets/img/cidade.png')
background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))

player_img = pygame.image.load('assets/img/player.png')
player_img = pygame.transform.scale(player_img, (SIZE, SIZE*1.5))

chao_img = pygame.image.load('assets/img/chao.png')
chao_img = pygame.transform.scale(chao_img, (SIZE,SIZE))

parede_img = pygame.image.load('assets/img/parede.png')
parede_img = pygame.transform.scale(parede_img, (SIZE, SIZE))

inimigo_img = pygame.image.load('assets/img/inimigo1.png')
inimigo_img = pygame.transform.scale(inimigo_img, (SIZE*(5/7), SIZE*(5/7)))

espinhos_img = pygame.image.load('assets/img/espinhos.png')
espinhos_img = pygame.transform.scale(espinhos_img, (SIZE, SIZE*0.5))

bolinha_img = pygame.image.load('assets/img/bola_de_fogo.png')
bolinha_img = pygame.transform.scale(bolinha_img, (SIZE, SIZE/2))

diamante_img = pygame.image.load('assets/img/diamante_vermelho.png')
diamante_img = pygame.transform.scale(diamante_img, (SIZE, SIZE))

moeda_img = pygame.image.load('assets/img/coin.png')
moeda_img = pygame.transform.scale(moeda_img, (SIZE, SIZE))

assets['background'] = background_img
assets['player'] = player_img
assets['chao'] = chao_img
assets['parede'] = parede_img
assets['monstro'] = inimigo_img
assets['espinhos'] = espinhos_img
assets['bola de fogo'] = bolinha_img
assets['diamante'] = diamante_img
assets['coin'] = moeda_img

groups= {}

groups['all_enemys'] = pygame.sprite.Group()
groups['all_blocks'] = pygame.sprite.Group()
groups['all_fireballs'] = pygame.sprite.Group()
groups['coins'] = pygame.sprite.Group()
groups['diamond'] = pygame.sprite.Group()


