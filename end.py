# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from config import *
from sprites import Button

def end_screen(window, screen):
    running = True
    
    if screen == 'WIN':
        telaFinal = pygame.image.load('assets/img/parabens.png')
    elif screen == 'LOSE':
        telaFinal = pygame.image.load('assets/img/gameover.png')
    telaFinal = pygame.transform.scale(telaFinal, (WIDTH, HEIGHT))
    

    buttons = [
        Button((415, 560, 210, 55), 'INIT'), # menu
    ]

    pygame.mixer.music.load('assets/sounds/Menu.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

    while running:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                state = 'QUIT'
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = 'QUIT'
                    running = False
                                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mousePos):
                        state = button.value
                        running = False

        # A cada loop, redesenha o fundo e os sprites
        window.blit(telaFinal, (0,0))

        # Depois de desenhar tudo, atualiza o display.
        pygame.display.update()

    return state