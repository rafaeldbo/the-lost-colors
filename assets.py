import pygame
from parameters import *

def load_assets(**kargs):
    corrent_colors = "_"
    if len(kargs) != 0:
        colors = kargs.get('colors')
        for color in colors:
            corrent_colors += color[0]
    path = f'assets/img/{corrent_colors}/'

    background_img = pygame.image.load(f'{path}cidade.png')
    background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))

    chao_img = pygame.image.load(f'{path}chao.png')
    chao_img = pygame.transform.scale(chao_img, (SIZE,SIZE))

    parede_img = pygame.image.load(f'{path}parede.png')
    parede_img = pygame.transform.scale(parede_img, (SIZE, SIZE))

    personagem_img = pygame.image.load(f'{path}personagem.png')
    personagem_img = pygame.transform.scale(personagem_img, (SIZE, SIZE*1.5))

    inimigo_img = pygame.image.load(f'{path}inimigoChao.png')
    inimigo_img = pygame.transform.scale(inimigo_img, (SIZE*(5/7), SIZE*(5/7)))

    espinhos_img = pygame.image.load(f'{path}espinhos.png')
    espinhos_img = pygame.transform.scale(espinhos_img, (SIZE, SIZE))

    moeda_img = pygame.image.load(f'{path}moeda.png')
    moeda_img = pygame.transform.scale(moeda_img, (SIZE, SIZE))

    bolinha_img = pygame.image.load(f'{path}bolaDeFogo.png')
    bolinha_img = pygame.transform.scale(bolinha_img, (SIZE, SIZE/2))

    diamante_img = pygame.image.load(f'assets/img/diamanteVermelho.png')
    diamante_img = pygame.transform.scale(diamante_img, (SIZE, SIZE))

    assets = {
        'background': background_img,
        'personagem': personagem_img,
        'chao': chao_img,
        'parede': parede_img,
        'inimigo chao': inimigo_img,
        'espinhos': espinhos_img,
        'bola de fogo': bolinha_img,
        'diamante': diamante_img,
        'moeda': moeda_img,
    }

    return assets
