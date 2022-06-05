# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from config import *
from functions import * 
from sprites import *
from assets import *

def fase_screen(window, fase):
    init_colors = FASES[fase]['required colors']
    if list(set(init_colors + COLORS)) == list(set(COLORS)):
        running = True

        checkpoint = 0

        assets = load_assets(fase, init_colors)
        player = Character(assets['personagem'], init_colors)
        groups = load_map(fase, assets, FASES[fase]['checkpoints'][checkpoint], init_colors)

        while running:
            clock.tick(FPS)
                
            # ----- Trata eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    state = 'QUIT'
                    running = False
                
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP) and (player.jump != 0) and (player.speedy >= 0): # Pulo
                        player.jump -= 1
                        player.speedy = -moviment_player_y

                    if event.key == pygame.K_SPACE: # Atirar bola de fogo
                        player.shoot(assets['bola de fogo'], groups)

                    if event.key == pygame.K_z: # Dar dash
                        player.dash()
                            
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP: # Para os movimentos
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.speedx = 0

            # Controle do Dash
            if player.in_dash:
                player.invencible = True
                now = pygame.time.get_ticks()
                elapsed_ticks = now - player.last_dash
                if elapsed_ticks >= player.dash_duration:
                    player.speedx = 0
                    player.in_dash = False
            else:
                player.invencible = False

            # Atualizando posições no jogo
            player.update()
            groups['all_sprites'].update(player)

            # Colisões entre o player e os blocos
            nearby_blocks = []
            for block in groups['all_blocks']:
                if (block.rect.left >= (player.rect.left - SIZE) and block.rect.right <= (player.rect.right + SIZE)) and (block.rect.top >= (player.rect.top - SIZE) and (block.rect.bottom <= player.rect.bottom + SIZE)):
                    nearby_blocks.append(block)
            collision_player_blocks = pygame.sprite.spritecollide(player, nearby_blocks, False)
            for bloco in collision_player_blocks:

                if bloco.rect.top < player.rect.top < bloco.rect.bottom and colisao_minima(player, bloco): # Colisão com o teto
                    player.rect.top = bloco.rect.bottom

                if bloco.rect.bottom > player.rect.bottom > bloco.rect.top and colisao_minima(player, bloco): # Colisão com o chão
                    player.rect.bottom = bloco.rect.top
                    player.jump = 2 if "blue" in player.colors else 1
                    player.speedy = 0

                if bloco.rect.bottom < ( player.rect.bottom + (SIZE/8)) and bloco.rect.bottom > (player.rect.top - (SIZE/8)): # Colisão com as laterais
                    player.go_right = not (bloco.rect.right > player.rect.right > bloco.rect.left)
                    player.go_left = not (bloco.rect.left < player.rect.left < bloco.rect.right)
                    # player.speedx = player.rect.right - bloco.rect.left
                    # groups['all_sprites'].update(player)
                    # player.speedx = 0
            
            # Movimenta na horizontal
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_RIGHT] and not player.in_dash:
                player.speedx = +moviment_player_x if player.go_right else 0
            elif pressed_keys[pygame.K_LEFT] and not player.in_dash:
                player.speedx = -moviment_player_x if player.go_left else 0
            
            # Verifica se o jogo perdeu uma vida
            hits = pygame.sprite.spritecollide(player, groups['all_enemys'], False, pygame.sprite.collide_mask)
            if (len(hits) != 0 and not player.invencible) or player.rect.top > HEIGHT:
                player.lifes -= 1
                groups = load_map(fase, assets, FASES[fase]['checkpoints'][checkpoint], player.colors)
                player.rect.bottom = FASES[fase]['checkpoints'][checkpoint]['chao']
            
            # Colisões dos inimigos
            collision_enemy_blocks = pygame.sprite.groupcollide(groups['all_enemys'], groups['all_blocks'], False, False)
            for monstro, blocos in collision_enemy_blocks.items():
                bloco = blocos[0]
                if monstro.direction == "horizontal":
                    if bloco.rect.right > monstro.rect.right > bloco.rect.left:
                        monstro.rect.right = bloco.rect.left
                        monstro.speed = -monstro.speed
                    elif bloco.rect.left < monstro.rect.left < bloco.rect.right:
                        monstro.rect.left = bloco.rect.right
                        monstro.speed = -monstro.speed
                
                if monstro.direction == "vertical":
                    if bloco.rect.top < monstro.rect.top < bloco.rect.bottom:
                        monstro.rect.top = bloco.rect.bottom 
                        monstro.speed = -monstro.speed          
                    elif bloco.rect.bottom > monstro.rect.bottom > bloco.rect.top:
                        monstro.rect.bottom = bloco.rect.top 
                        monstro.speed = -monstro.speed

            # Colisões da bola de fogo
            collision_breakables_fireball = pygame.sprite.groupcollide(groups['breakables'], groups['all_fireballs'], True, True, pygame.sprite.collide_mask)
            player.points += 100*len(collision_breakables_fireball)
            pygame.sprite.groupcollide(groups['all_blocks'], groups['all_fireballs'], False, True)

            # Colisões com as moedas e prismas (coletáveis)
            collision_player_collectibles = pygame.sprite.spritecollide(player, groups['collectibles'], True, pygame.sprite.collide_mask)
            for collected in collision_player_collectibles:
                player.points += 100
                if collected.color != None: # Verifica se é um diamante
                    player.colors.append(collected.color) # Coleta a cor

                    # Recarrega o mapa segundo o novo checkpoint
                    checkpoint += 1
                    groups = load_map(fase, assets, FASES[fase]['checkpoints'][checkpoint], player.colors)

                    # Atualiza as cores do jogo
                    assets = load_assets(fase, player.colors)
                    player.update_color(assets)
                    player.rect.bottom = FASES[fase]['checkpoints'][checkpoint]['chao']
                    for entity in groups['all_sprites']:
                        entity.update_color(assets)

            # Colisão com a bandeira (Verifica se o jogador ganhou o jogo)
            collision_player_flag = pygame.sprite.spritecollide(player, groups['flag'], False, pygame.sprite.collide_mask)
            if len(collision_player_flag) != 0:
                colors = COLORS
                colors = player.colors
                FASES['FASE1']['pontuação'] = player.points
                state = 'WIN'
                running = False

            # Verifica se o jogador perdeu o jogo
            if player.lifes <= 0:
                state = 'LOSE'
                running = False
                
            # ----- Gera saídas
            window.blit(assets['background'], (0,0))
            window.blit(player.image, player.rect)
            groups['all_sprites'].draw(window)

        # Depois de desenhar tudo, atualiza o display.
            pygame.display.update()

        return state
    else:
        return 'INIT'