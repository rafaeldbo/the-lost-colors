import pygame
from config import *

"""
Toda vez que o jogador pega um prisma, os assets são atualizados para que as imagens fiquem com as cores refertes aquele
prisma. As imagens de cada prisma estão organizadas em uma pasta cujo nome é composto pelas cores dos prismas coletados
"""
# Função que carrega os arquivos do jogo (imagens, sons e fontes)
def load_assets(fase, corrent_colors):

    # Gera o novo diretório para acessas as imagens referente aos cores dos prismas coletados
    colors_path = "_"
    if len(corrent_colors) != 0:
        for color in corrent_colors:
            colors_path += color[0]
    path = f'assets/img/{colors_path}/'

    # Carrega o fundo, o chão e as paredes dependendo da fase atual
    background_img = pygame.image.load(f"{path}{GAME[fase]['assets'][0]}.png")
    background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))

    chao_img = pygame.image.load(f"{path}{GAME[fase]['assets'][1]}.png")
    chao_img = pygame.transform.scale(chao_img, (SIZE,SIZE))

    parede_img = pygame.image.load(f"{path}{GAME[fase]['assets'][2]}.png")
    parede_img = pygame.transform.scale(parede_img, (SIZE, SIZE))

    # Carrega e organiza as imagens da animação do personagem
    personagem_img = pygame.image.load(f'{path}/personagem/parado.png')
    personagem_img = pygame.transform.scale(personagem_img, (SIZE, SIZE*1.5))
    personagem_anim = []
    for i in range(2):
        img = pygame.image.load(f'{path}/personagem/{i}.png')
        img = pygame.transform.scale(img, (SIZE, 1.5*SIZE))
        personagem_anim.append(img)
    
    caixa_img = pygame.image.load(f'{path}caixa.png')
    caixa_img = pygame.transform.scale(caixa_img, (SIZE,SIZE))

    inimigo_img = pygame.image.load(f'{path}inimigoChao.png')
    inimigo_img = pygame.transform.scale(inimigo_img, (SIZE*(5/7), SIZE*(5/7)))

    espinhos_img = pygame.image.load(f'{path}espinhos.png')
    espinhos_img = pygame.transform.scale(espinhos_img, (SIZE, SIZE))

    moeda_img = pygame.image.load(f'{path}moeda.png')
    moeda_img = pygame.transform.scale(moeda_img, (SIZE, SIZE))

    foguinho_img = pygame.image.load(f'{path}bolaDeFogo.png')
    foguinho_img = pygame.transform.scale(foguinho_img, (SIZE, SIZE/2))
    
    botao_img = pygame.image.load(f'assets/img/botao.png')
    botao_img = pygame.transform.scale(botao_img, (40, 40))

    prisma_green = pygame.image.load(f'assets/img/prisma_green.png')
    prisma_green = pygame.transform.scale(prisma_green, (SIZE*(5/7), SIZE*(5/7)))

    prisma_blue = pygame.image.load(f'assets/img/prisma_blue.png')
    prisma_blue = pygame.transform.scale(prisma_blue, (SIZE*(5/7), SIZE*(5/7)))

    prisma_red = pygame.image.load(f'assets/img/prisma_red.png')
    prisma_red = pygame.transform.scale(prisma_red, (SIZE*(5/7), SIZE*(5/7)))
    
    # carrega a fonte de texto usada no jogo
    score_font = pygame.font.Font((f'assets/font/base.ttf'), 28)

    # Carrega e organiza as imagens da animação da bandeira
    bandeira_img = pygame.image.load(f'assets/img/bandeira.png')
    bandeira_img = pygame.transform.scale(bandeira_img, (SIZE, SIZE*2))
    bandeira_anim = []
    for i in range(4):
        img = pygame.image.load(f'assets/img/bandeira/{i}.png')
        img = pygame.transform.scale(img, (SIZE, SIZE*2))
        bandeira_anim.append(img)
    checkpoint_img = pygame.image.load(f'assets/img/checkpoint.png')
    checkpoint_img = pygame.transform.scale(checkpoint_img, (SIZE, SIZE*2))

    # Carrega e organiza as imagens da animação da explosão
    explosion_img = pygame.image.load(f'assets/img/explosao.png')
    explosion_img = pygame.transform.scale(explosion_img, (SIZE, SIZE))
    explosion_anim = []
    for i in range(9):
        # Os arquivos de animação são numerados de 00 a 08
        img = pygame.image.load(f'assets/img/explosao/{i}.png')
        img = pygame.transform.scale(img, (70, 70))
        explosion_anim.append(img)

    # gera o dicionário de assets
    assets = {
        'background': background_img,
        'personagem': personagem_img,
        'animacao personagem': personagem_anim,
        'chao': chao_img,
        'parede': parede_img,
        'inimigo chao': inimigo_img,
        'espinhos': espinhos_img,
        'bola de fogo': foguinho_img,
        'moeda': moeda_img,
        "caixa" : caixa_img,
        "bandeira": bandeira_img,
        "animacao bandeira": bandeira_anim,
        "checkpoint": checkpoint_img,
        "explosao": explosion_img,
        "animacao explosao": explosion_anim,
        "botao": botao_img,
        "prisma_green": prisma_green,
        "prisma_blue": prisma_blue,
        "prisma_red": prisma_red,

        "score_font" : score_font,

        # carrega os efeitos sonoros do jogo
        'moeda som': pygame.mixer.Sound('assets/sounds/Coin.ogg'),
        "dash som": pygame.mixer.Sound('assets/sounds/Dash.ogg'),
        'explode som': pygame.mixer.Sound('assets/sounds/Explode.ogg'),
        "hit som": pygame.mixer.Sound('assets/sounds/Hit.ogg'),
        "pulo som": pygame.mixer.Sound('assets/sounds/Jump.ogg'),
    }

    return assets