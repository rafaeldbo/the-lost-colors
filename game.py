# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from config import *
from init import init_screen
from fase import fase_screen
from end import end_screen

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT)) # SIZE da tela
pygame.display.set_caption('The lost colors') # título da tela

state = 'INIT'
while state != 'QUIT':
    if state == 'INIT':
        state= init_screen(window)
    if 'FASE' in state:
        GAME, state = fase_screen(window, state)
    if state in ['WIN', 'LOSE']:
        state = end_screen(window, state)

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados