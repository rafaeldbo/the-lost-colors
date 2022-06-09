# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from config import *
from sprites import Button

# Função que cria o Menu de ínicio
def init_screen(window):
    running = True
    state = 'INIT'

    # Declaração da imagens e das váriasvas da animação do menu
    telaInicial = pygame.image.load('assets/img/menu1.png')
    time_frame = [0.2*second, 0.5*second, 0.2*second, 0.1*second, 0.05*second, 0.6*second, 10*second] # lista de duração de cada frame
    last_update = 0
    frame = 0

    # Declaração dos botões
    buttons = [
        Button((305, 350, 210, 210), 'FASE1'), # Iniciar fase da floresta
        Button((537, 350, 210, 210), 'FASE2'), # Iniciar fase do laborátorio
    ]
    
    while running:
        clock.tick(FPS)

    # ----- Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                state = 'QUIT'
                running = False
            # Se estiver na tela de instruções, espera o jogador apertar qualquer tecla
            if event.type == pygame.KEYDOWN and state != 'INIT':
                running = False # Fecha o menu
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Se estiver no menu iniciar, espera o jogador apertar em um botão
                if state == 'INIT':
                    mousePos = pygame.mouse.get_pos()
                    for button in buttons:
                        # Inicia uma fase do jogo
                        if button.rect.collidepoint(mousePos):
                            state = button.value
                            # Exibe tela de instruções
                            telaInicial = pygame.image.load('assets/img/instrucoes.png')
                else:
                    running = False # Fecha o menu

        # Caso esteja no menu de início, anima o menu
        if state == 'INIT':
            now = pygame.time.get_ticks()
            elapsed_ticks = now - last_update
            if elapsed_ticks > time_frame[frame]:
                last_update = now
                frame = 1 if frame == 0 else 0 # varia entre o 1° e o 2° frame da animação
                telaInicial = pygame.image.load(f'assets/img/menu{frame}.png')

        # A cada loop, redesenha o fundo e os sprites
        window.blit(telaInicial, (0,0))

        # Depois de desenhar tudo, atualiza o display.
        pygame.display.update()

    return state