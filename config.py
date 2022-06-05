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
moviment_player_y = 50

moviment_enemy = 5

moviment_fireball = 15

# Fases
COLORS = []

FASES = {
    'FASE1': {
        'assets': ['floresta', 'grama', 'terra'],
        'pontuação': 0,
        'pontuação total': 0,
        'inimigos mortos': 0,
        'inimigos totais': 0,
        'moedas coletadas': 0,
        'moedas totais': 0,
        'checkpoints': [
            {'inicio': 0, 'fim': 89, 'chao': HEIGHT - SIZE},
            {'inicio': 67, 'fim': 180, 'chao': HEIGHT - SIZE},
            {'inicio': 194, 'fim': 344, 'chao': HEIGHT - 4*SIZE},
        ]
    },
    'FASE2': {
        'assets': ['laboratorio', 'piso', 'parede'],
        'pontuação': 0,
        'pontuação total': 0,
        'inimigos mortos': 0,
        'inimigos totais': 0,
        'moedas coletadas': 0,
        'moedas totais': 0,
        'checkpoints': [
            {'inicio': 0, 'fim': 100, 'chao': HEIGHT - 2*SIZE},
            #{'inicio': 0, 'fim': 0},
        ]
    }
}

