# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from sympy import sec
from config import *
from sprites import Button

def init_screen(window):
    running = True
    
    telaInicial = pygame.image.load('assets/img/menu1.png')
    time_frame = [0.2*second, 0.5*second, 0.2*second, 0.1*second, 0.05*second, 0.6*second, 10*second]
    last_frame_time = 0
    frame = 0
    buttons = [
        Button((305, 350, 210, 210), 'FASE1'), # fase floresta
        Button((537, 350, 210, 210), 'FASE2'), # fase lab
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

        now = pygame.time.get_ticks()
        elapsed_ticks = now - last_frame_time
        if elapsed_ticks > time_frame[frame]:
            frame = frame+1 if frame < len(time_frame)-1 else 0
            last_frame_time = now
            frame_image = 1 if frame%2 != 0 else 2
            telaInicial = pygame.image.load(f'assets/img/menu{frame_image}.png')

        # A cada loop, redesenha o fundo e os sprites
        window.blit(telaInicial, (0,0))

        # Depois de desenhar tudo, atualiza o display.
        pygame.display.update()

    return state