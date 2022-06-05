import pygame
from config import *

def load_assets(fase, corrent_colors):
    colors_path = "_"
    if len(corrent_colors) != 0:
        for color in corrent_colors:
            colors_path += color[0]
    path = f'assets/img/{colors_path}/'
    path_font = f'assets/font/'

    background_img = pygame.image.load(f"{path}{FASES[fase]['assets'][0]}.png")
    background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))

    chao_img = pygame.image.load(f"{path}{FASES[fase]['assets'][1]}.png")
    chao_img = pygame.transform.scale(chao_img, (SIZE,SIZE))

    parede_img = pygame.image.load(f"{path}{FASES[fase]['assets'][2]}.png")
    parede_img = pygame.transform.scale(parede_img, (SIZE, SIZE))
    
    caixa_img = pygame.image.load(f'{path}caixa.png')
    caixa_img = pygame.transform.scale(caixa_img, (SIZE,SIZE))

    personagem_img = pygame.image.load(f'{path}personagem.png')
    personagem_img = pygame.transform.scale(personagem_img, (SIZE, SIZE*1.5))

    inimigo_img = pygame.image.load(f'{path}inimigoChao.png')
    inimigo_img = pygame.transform.scale(inimigo_img, (SIZE*(5/7), SIZE*(5/7)))

    espinhos_img = pygame.image.load(f'{path}espinhos.png')
    espinhos_img = pygame.transform.scale(espinhos_img, (SIZE, SIZE))

    moeda_img = pygame.image.load(f'{path}moeda.png')
    moeda_img = pygame.transform.scale(moeda_img, (SIZE, SIZE))

    foguinho_img = pygame.image.load(f'{path}bolaDeFogo.png')
    foguinho_img = pygame.transform.scale(foguinho_img, (SIZE, SIZE/2))

    score_font = pygame.font.Font((f'{path_font}PressStart2P.ttf'), 28)

    bandeira_anim = []
    for i in range(4):
        img = pygame.image.load(f'assets/img/bandeira/{i}.png')
        img = pygame.transform.scale(img, (SIZE, 2*SIZE))
        bandeira_anim.append(img)

    assets = {
        'background': background_img,
        'personagem': personagem_img,
        'chao': chao_img,
        'parede': parede_img,
        'inimigo chao': inimigo_img,
        'espinhos': espinhos_img,
        'bola de fogo': foguinho_img,
        'moeda': moeda_img,
        "caixa" : caixa_img,
        "bandeira": bandeira_anim,
        "score_font" : score_font
    }

    return assets
