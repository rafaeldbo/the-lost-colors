import pygame
from parameters import *

def init_screen(window):
    running = True

    telaInicial = pygame.image.load('assets/img/menu1.png')
    time_frame = [200, 500, 100, 50, 200, 600, 7000]
    last_frame_time = 0
    frame = 0
    button_floresta = pygame.Rect(305, 350, 210, 210)
    button_lab = pygame.Rect(537, 350, 210, 210)

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
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if button_floresta.right >= mouseX >= button_floresta.left and button_floresta.bottom >= mouseY >= button_floresta.top:
                    state = 'FASE1'
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

        # Depois de desenhar tudo, inverte o display.
        pygame.display.update()

    return state