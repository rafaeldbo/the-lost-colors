# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from config import *
from sprites import Button
from assets import *

def end_screen(window, DATA, screen, fase):
    running = True

    assets = load_assets(fase, GAME[fase]['required colors'])
    score_color = COLORS['white']
    points = DATA[fase]['pontuacao']

    if screen == 'WIN':
        telaFinal = pygame.image.load('assets/img/parabens.png')

        score_color = COLORS['yellow']
        best_score = DATA[fase]['melhor pontuacao']
        best_score = assets['score_font'].render(f"melhor pontuação:{best_score:04d}", True, )
        best_score_rect = best_score.get_rect()
        best_score_rect.midtop = (WIDTH/2,  HEIGHT/2 + 90)

    elif screen == 'LOSE':
        telaFinal = pygame.image.load('assets/img/gameover.png')

    telaFinal = pygame.transform.scale(telaFinal, (WIDTH, HEIGHT))

    # Desenhando o score
    score = assets['score_font'].render(f"pontuação:{points:04d}", True, score_color)
    score_rect = score.get_rect()
    score_rect.midtop = (WIDTH/2,  HEIGHT/2 + 50)

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
                if event.key == pygame.K_RETURN:
                    state = 'INIT'
                    running = False
                                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mousePos):
                        state = button.value
                        running = False

        # A cada loop, redesenha o fundo e os sprites
        window.blit(telaFinal, (0,0))
        window.blit(score, score_rect) # score
        if screen == 'WIN':
            window.blit(best_score, best_score_rect)

        # Depois de desenhar tudo, atualiza o display.
        pygame.display.update()

    return state