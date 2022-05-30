import pygame
from assets import *
from parameters import FPS

def init_screen(window):
    
    assets = load_assets()
    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(FPS)

    # ----- Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                state = 'QUIT'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = 'FASE1'
                    running = False

        # A cada loop, redesenha o fundo e os sprites
        window.blit(assets['background'], (0,0))

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state