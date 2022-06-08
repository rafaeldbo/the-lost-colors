import pygame, io, json

# Tempo
clock = pygame.time.Clock()
FPS = 30 
second = 1000
frame = second/FPS

# Constantes
gravidade = 8

# Tamanhos
SIZE = 70
WIDTH = SIZE*15
HEIGHT = SIZE*10

# Cores
COLORS = {'black': (0,0,0), 'white': (255,255,255), 'yellow': (255,255,0), 'red': (255,0,0)}

# Movimentos
moviment_player_x = 12
moviment_player_y = 55

moviment_enemy = 5

moviment_fireball = 15

# Dados das Fases
GAME = {
    'FASE1': {
        'assets': ['floresta', 'grama', 'terra'],
        'required colors': [],
        'pontuacao total': 9300,
        'checkpoints': [
            {'inicio': 0, 'fim': 89, 'chao': HEIGHT - SIZE, 'parede': SIZE*3}, # começo da fase
            {'inicio': 67, 'fim': 237, 'chao': HEIGHT - SIZE, 'parede': SIZE*3}, # diamante verde
            {'inicio': 67, 'fim': 237, 'chao': HEIGHT - SIZE*6, 'parede': SIZE*89}, # bandeira 1
            {'inicio': 199, 'fim': 348, 'chao': HEIGHT - SIZE, 'parede': SIZE*19}, # diamante azul
            {'inicio': 199, 'fim': 348, 'chao': HEIGHT - SIZE*6, 'parede': SIZE*133}, # final da fase
        ]
    },
    'FASE2': {
        'assets': ['laboratorio', 'piso', 'parede'],
        'required colors': ['green', 'blue'],
        'pontuacao total': 7100,
        'checkpoints': [
            {'inicio': 0, 'fim': 70, 'chao': HEIGHT - SIZE, 'parede': SIZE*3}, # começa da fase
            {'inicio': 51, 'fim': 247, 'chao': HEIGHT - SIZE*2, 'parede': SIZE*3}, # diamante vermelho
            {'inicio': 115, 'fim': 247, 'chao': HEIGHT - SIZE*2, 'parede': SIZE*10}, # bandeira 1
            {'inicio': 115, 'fim': 255, 'chao': HEIGHT - SIZE*8, 'parede': SIZE*196}, # final da fase
        ]
    }
}

# Dados do jogador
DATA = {
    'colors': ['green', 'blue'],
    'FASE1': {
        'pontuacao': 0,
        'melhor pontuacao': 0,
    },
    'FASE2': {
        'pontuacao': 0,
        'melhor pontuacao': 0,
    }
}

with io.open('assets/save.json', "r", encoding='utf8"') as file:
    data = file.read()
DATA = json.loads(data)


