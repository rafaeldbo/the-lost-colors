# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from parameters import *
from init import *
from fase1 import *
from exit_game import *

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT)) # SIZE da tela
pygame.display.set_caption('The lost colors') # título da tela

state = 'INIT'

while state != 'QUIT':
    if state == 'INIT':
        state= init_screen(window)
    if state == 'FASE1':
        state = fase1_screen(window)
    if state == 'END':
        state = end_screen(window)
        
pygame.quit()
    
# ===== Finalização =====
  # Função do PyGame que finaliza os recursos utilizados