# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from config import *
from functions import save
from init import init_screen
from fase import fase_screen 
from end import end_screen

pygame.init()
pygame.mixer.init()

# Toca a música
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
        # Inicia a fase
        DATA, state, fase = fase_screen(window, DATA, state)
    if state in ['WIN', 'LOSE']:
        # Exibe a tela final
        # A tela exibida muda dependendo se o jogador ganhou ou perdeu o jogo
        state = end_screen(window, DATA, state, fase)

save(DATA)
# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados