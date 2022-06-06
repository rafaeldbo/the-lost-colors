import pygame

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

# Movimentos
moviment_player_x = 12
moviment_player_y = 55

moviment_enemy = 5

moviment_fireball = 15

# Fases

GAME = {
    'colors': ['green', 'blue'],
    'FASE1': {
        'assets': ['floresta', 'grama', 'terra'],
        'required colors': [],
        'pontuação': 0,
        'pontuação total': 0,
        'inimigos mortos': 0,
        'inimigos totais': 0,
        'moedas coletadas': 0,
        'moedas totais': 0,
        'checkpoints': [
            {'inicio': 0, 'fim': 89, 'chao': HEIGHT - SIZE, 'parede': SIZE*3},
            {'inicio': 67, 'fim': 237, 'chao': HEIGHT - SIZE, 'parede': SIZE*3},
            {'inicio': 199, 'fim': 348, 'chao': HEIGHT - SIZE, 'parede': SIZE*19},
        ]
    },
    'FASE2': {
        'assets': ['laboratorio', 'piso', 'parede'],
        'required colors': ['green', 'blue'],
        'pontuação': 0,
        'pontuação total': 0,
        'inimigos mortos': 0,
        'inimigos totais': 0,
        'moedas coletadas': 0,
        'moedas totais': 0,
        'checkpoints': [
            {'inicio': 0, 'fim': 70, 'chao': HEIGHT - SIZE, 'parede': SIZE*3},
            {'inicio': 51, 'fim': 247, 'chao': HEIGHT - SIZE*2, 'parede': SIZE*3},
        ]
    }
}

