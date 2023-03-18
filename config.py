import pygame, io, json

# Tempo
CLOCK = pygame.time.Clock()
FPS = 30 # frames por segundo
SECOND = 1000 # segundo
FRAME = SECOND/FPS # tempo de 1 frame

# Gravidade do jogo
GRAVIDADE = 8 

# Tamanhos
SIZE = 70 # Tamanho padrão de um bloco
WIDTH = SIZE*15 # Largura da Janela do Jogo
HEIGHT = SIZE*10 # Altura da Janela do jogo

# Cores
COLORS = {'black': (0,0,0), 'white': (255,255,255), 'yellow': (255,255,0), 'red': (255,0,0)} 

# Variaveis globais do player
MAX_LIFES = 3 # Quantidade máxima de vidas do player

PLAYER_SPEED = 12 # Velocidade base do player na horizontal
PLAYER_SPEED_JUMP = 55 # Velocidade base do player na vertical

DASH_DELAY = 4000 # Delay do Dash do player
DASH_SPEED = 65 # Velocidade do uso do Dash do player
DASH_DURATION = FRAME*3 # Duração do Dash do player

SHOOT_DELAY = 500 # Delay do uso da bola de fogo
FIREBALL_SPEED = 15 # Velocidade da bola de fogo

# Outras variaiveis globais
ENEMY_SPEED = 5 # Velocidade base dos inimigos (horizontal e vertical)
COIN_POINTS = 100 # Quantidade de pontos de uma moeda
NEW_LIFE_POINTS = 2000 # QUantidade de pontos necessários para ganhar uma vida

# Conversor de direção
DIRECTION = {
    'right': +1,
    'left': -1
}

# Dados das Fases
GAME = {
    'FASE1': {
        'nome': 'floresta', # Nome da Fase
        'required colors': [], # Cores requeridas para começar a fase
        'pontuacao total': 9300, # pontuação máxima da fase (coletando todas as moedas)
        'checkpoints': [ # Lista de checkpoints da fase
            {'inicio': 0, 'fim': 89, 'chao': HEIGHT - SIZE, 'parede': SIZE*3}, # Começo da fase
            {'inicio': 67, 'fim': 237, 'chao': HEIGHT - SIZE, 'parede': SIZE*3}, # Diamante verde
            {'inicio': 67, 'fim': 237, 'chao': HEIGHT - SIZE*6, 'parede': SIZE*89}, # Bandeira 1
            {'inicio': 199, 'fim': 348, 'chao': HEIGHT - SIZE, 'parede': SIZE*19}, # Diamante azul
            {'inicio': 199, 'fim': 348, 'chao': HEIGHT - SIZE*6, 'parede': SIZE*133}, # Final da fase
        ]
    },
    'FASE2': {
        'nome': 'laboratorio', # Nome da Fase
        'required colors': ['green', 'blue'], # Cores requeridas para começar a fase
        'pontuacao total': 7100, # pontuação máxima da fase (coletando todas as moedas)
        'checkpoints': [ # Lista de checkpoints da fase 
            {'inicio': 0, 'fim': 70, 'chao': HEIGHT - SIZE, 'parede': SIZE*3}, # Começo da fase
            {'inicio': 51, 'fim': 247, 'chao': HEIGHT - SIZE*2, 'parede': SIZE*3}, # Diamante vermelho
            {'inicio': 115, 'fim': 247, 'chao': HEIGHT - SIZE*2, 'parede': SIZE*10}, # Bandeira 1
            {'inicio': 115, 'fim': 255, 'chao': HEIGHT - SIZE*8, 'parede': SIZE*196}, # Final da fase
        ]
    }
}

# Dados do jogador
DATA = {
    'cores': ['green', 'blue'], # Cores coletadas pelo jogador
    'FASE1': {
        'pontuacao': 0, # Última pontuação na fase 1
        'melhor pontuacao': 0, # Merlhor pontuação na fase 1
    },
    'FASE2': {
        'pontuacao': 0, # Última pontuação na fase 2
        'melhor pontuacao': 0, # Merlhor pontuação na fase 2
    }
}

# Extrai os doados do jogador salvos no save.json
with io.open('assets/save.json', "r", encoding='utf8"') as file:
    data = file.read()
DATA = json.loads(data)


