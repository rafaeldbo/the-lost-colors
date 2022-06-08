# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from config import *
from init import init_screen
from fase import fase_screen
from end import end_screen

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('assets/sounds/Menu.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT)) # SIZE da tela
pygame.display.set_caption('The lost colors') # título da tela

state = 'INIT'
while state != 'QUIT':
    if state == 'INIT':
        state = init_screen(window)
    if 'FASE' in state:
        GAME, state, fase = fase_screen(window, state, GAME)
    if state in ['WIN', 'LOSE']:
        state = end_screen(window, state, fase, GAME)

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados