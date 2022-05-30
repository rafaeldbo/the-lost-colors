import pygame
from assets import *
from parameters import FPS

def end_screen(window):
    assets = load_assets()
    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(FPS)
        # ----- Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                state = 'QUIT'
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = 'FASE1'
                    running = False
                if event.key == pygame.K_ESCAPE:
                    state = 'QUIT'
                    running = False

        window.blit(assets['background'], (0,0))
        pygame.display.flip()

    return state