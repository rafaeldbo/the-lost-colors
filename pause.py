# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from config import *
from sprites import Button

def pause_screen(window, fase):
    running = True
    
    telaPause = pygame.image.load('assets/img/pause.png')

    buttons = [
        Button((370, 220, 300, 70), 'CONTINUE'), # continuar
        Button((370, 300, 300, 70), 'INIT'), # sair
        Button((370, 380, 300, 70), fase), # recomeçar
    ]
    
    while running:
        clock.tick(FPS)

    # ----- Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                state = 'QUIT'
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = 'CONTINUE'
                    running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mousePos):
                        state = button.value
                        running = False

        # A cada loop, redesenha o fundo e os sprites
        window.blit(telaPause, (0,0))

        # Depois de desenhar tudo, atualiza o display.
        pygame.display.update()

    return state