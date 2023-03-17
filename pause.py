# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from config import *
from sprites import Button

def pause_screen(window, fase):
    running = True
    
    # Define a tela do pause
    telaPause = pygame.image.load('assets/img/pause.png')

    buttons = [
        Button((370, 220, 300, 70), 'CONTINUE'), # Botão de continuar a jogar
        Button((370, 300, 300, 70), 'INIT'), # Botão de voltar ao menu inicial (sair)
        Button((370, 380, 300, 70), fase), # botão de recomeçar a fase
    ]
    
    while running:
        CLOCK.tick(FPS)

    # ----- Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                state = 'QUIT'
                running = False
            if event.type == pygame.KEYDOWN:
                # Se o jogador apertar "esc", despausa o jogo
                if event.key == pygame.K_ESCAPE:
                    state = 'CONTINUE'
                    running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Espera o jogador apertar um botão
                mousePos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mousePos):
                        # Executa a função do botão
                        state = button.value
                        running = False
                        if state == 'INIT': # Se for retornar ao menu, inicia a música do menu
                            pygame.mixer.music.load('assets/sounds/Menu.mp3')
                            pygame.mixer.music.set_volume(0.4)
                            pygame.mixer.music.play(loops=-1)

        # A cada loop, redesenha o fundo e os sprites
        window.blit(telaPause, (0,0))

        # Depois de desenhar tudo, atualiza o display.
        pygame.display.update()

    return state