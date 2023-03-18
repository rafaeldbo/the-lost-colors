# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from config import *
from functions import * 
from sprites import *
from assets import *
from pause import pause_screen

def fase_screen(window, DATA, fase):
    init_colors = list(GAME[fase]['required colors'])
    if list(set(init_colors + DATA['cores'])) == list(set(DATA['cores'])):
        # Verifica se o jogador tem as cores necessárias para entrar na fase
        running = True

        assets = load_assets(fase, init_colors) # Carrega os arquivos iniciais
        player = Character(assets, init_colors) # Cria o Personagem

        # Gera o mapa no primeiro checkpoint
        groups = load_map(assets, player, fase)
        pause_button = Button((15, 15, 40, 40), 'PAUSE', image=assets['botao']) # Botão de pause

        pygame.mixer.music.load(f'assets/sounds/{fase}.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)
        # Toca musica da fase

        while running:
            CLOCK.tick(FPS)
                
            # ----- Trata eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    state = 'QUIT'
                    running = False
                
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP) and (player.jump != 0) and (player.speedy >= 0): 
                        # Pulo
                        player.jump -= 1
                        player.speedy = -PLAYER_SPEED_JUMP
                        assets['pulo som'].play()

                    if event.key == pygame.K_SPACE: # Atirar bola de fogo
                        player.shoot(assets, groups)

                    if event.key == pygame.K_z: # Dar dash
                        player.dash(assets)

                    if event.key == pygame.K_ESCAPE: # Pause
                        state = pause_screen(window, fase)
                        running = (state == 'CONTINUE')
                            
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP: 
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]: 
                        # Para os movimentos no eixo x
                        player.speedx = 0
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Abre a tela de pause
                    mousePos = pygame.mouse.get_pos()
                    if pause_button.rect.collidepoint(mousePos):
                        state = pause_screen(window, fase)
                        running = (state == 'CONTINUE')

            # Controle do Dash
            if player.in_dash:
                dash, last = player.delay(DASH_DURATION, player.last_dash)
                if dash:
                    player.speedx = 0
                    player.in_dash = False

            # Atualizando posições no jogo
            player.update()
            groups['all_sprites'].update(player)

            # Colisões entre o player e os blocos
            collision_player_blocks = pygame.sprite.spritecollide(player, groups['blocks'], False)
            for bloco in collision_player_blocks:
                
                # Colisão com o teto
                if bloco.rect.top < player.rect.top < bloco.rect.bottom and colisao_minima(player, bloco):
                    player.rect.top = bloco.rect.bottom

                # Colisão com o chão, impede que o player caia
                if bloco.rect.bottom > player.rect.bottom > bloco.rect.top and colisao_minima(player, bloco):
                    player.rect.bottom = bloco.rect.top
                    # Restaura o numero de pulos, pulo duplo se tiver coletado o prisma azul
                    player.jump = 2 if "blue" in player.colors else 1
                    player.speedy = 0

                # Colisão com as laterais, impede que o player atravesse o bloco
                if bloco.rect.top < (player.rect.bottom - (SIZE/8)) and bloco.rect.bottom > (player.rect.top + (SIZE/8)):
                    # Se o player está antes do bloco
                    if player.rect.right > bloco.rect.left > player.rect.left:
                        player.speedx = -(player.rect.right - bloco.rect.left)
                    # Se o player está depois do bloco
                    elif  player.rect.left < bloco.rect.right < player.rect.right:
                        player.speedx = bloco.rect.right - player.rect.left
                    # Se o player estiver em dash, encerra o dash
                    if player.in_dash:
                        player.in_dash = False
                    groups['all_sprites'].update(player)
                    player.speedx = 0
            
            # Movimenta na horizontal
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_RIGHT] and not player.in_dash:
                player.speedx = +PLAYER_SPEED 
            elif pressed_keys[pygame.K_LEFT] and not player.in_dash:
                player.speedx = -PLAYER_SPEED
            
            # Colisão entre Personagem e "causadores de dano"
            hits = pygame.sprite.spritecollide(player, groups['damagers'], False, pygame.sprite.collide_mask)
            # Verifica se o jogador perdeu uma vida
            if (len(hits) != 0 and not player.in_dash) or player.rect.top > HEIGHT:
                player.lifes -= 1
                assets["hit som"].play()
                # Recarrega o mapa enviando o player para o checkpoint
                groups = load_map(assets, player, fase)
                player.rect.bottom = GAME[fase]['checkpoints'][player.checkpoint]['chao']
            
            # Colisões dos monstros com os blocos (vertical e horizontal)
            collision_monster_blocks = pygame.sprite.groupcollide(groups['enemys'], groups['blocks'], False, False)
            for enemy, blocos in collision_monster_blocks.items():
                bloco = blocos[0]

                # Se o montro se movimenta na horizontal
                if enemy.speedx != 0:
                    # Se houve colisão reposiciona o enemy, impede que ele atravesse o bloco
                    # Inverte a direção da velocidade
                    if bloco.rect.right > enemy.rect.right > bloco.rect.left:
                        enemy.rect.right = bloco.rect.left
                    elif bloco.rect.left < enemy.rect.left < bloco.rect.right:
                        enemy.rect.left = bloco.rect.right
                    enemy.speedx = -enemy.speedx

                # Se o enemy se movimenta na vertical
                if enemy.speedy != 0:
                    # Se houve colisão reposiciona o enemy, impede que ele atravesse o bloco
                    # Inverte a direção da velocidade
                    if bloco.rect.top < enemy.rect.top < bloco.rect.bottom:
                        enemy.rect.top = bloco.rect.bottom
                    elif bloco.rect.bottom > enemy.rect.bottom > bloco.rect.top:
                        enemy.rect.bottom = bloco.rect.top 
                    enemy.speedy = -enemy.speedy

            # Colisões da bola de fogo com os breakables
            # Quando o enemy ou a caixa é atingida gera a explosão
            collision_breakables_fireballs = pygame.sprite.groupcollide(groups['breakables'], groups['fireballs'], True, True, pygame.sprite.collide_mask)
            for element in collision_breakables_fireballs:
                explosao = Explosion(assets, element.rect.centerx, element.rect.centery)
                groups['all_sprites'].add(explosao)
            pygame.sprite.groupcollide(groups['blocks'], groups['fireballs'], False, True)

            # Colisões com as moedas e prismas (coletáveis)
            collision_player_collectibles = pygame.sprite.spritecollide(player, groups['collectibles'], True, pygame.sprite.collide_mask)
            for collected in collision_player_collectibles:
                player.collected.append(collected.index)

                if type(collected) == Coin: # Verifica se é uma moeda
                    player.points += 100
                    if player.points%2000 == 0 and player.lifes < 3:
                        player.lifes += 1
                    assets["moeda som"].play()

                elif type(collected) == Prism: # Verifica se é um diamante
                    assets, player = collected.update_assets_color(assets, player, fase)
                
                if issubclass(type(collected), Checkpoint): # Verifica se é um checkpoint
                    # Recarrega o mapa segundo o novo checkpoint
                    player.checkpoint = player.checkpoint+1 if player.checkpoint < len(GAME[fase]['checkpoints'])-1 else 0
                    groups = load_map(assets, player, fase)
                    player.rect.bottom = GAME[fase]['checkpoints'][player.checkpoint]['chao']

            # verifica se o jogador ganhou o jogo
            if player.checkpoint == len(GAME[fase]['checkpoints'])-1:
                # Armazena os prismas/cores coletadas
                DATA['cores'] = player.colors
                # Armazena a pontuação
                DATA[fase]['pontuacao'] = player.points
                if player.points > DATA[fase]['melhor pontuacao']:
                    DATA[fase]['melhor pontuacao'] = player.points
                # Muda o estado do jogo e da fase
                state = 'WIN'
                running = False
            
            # Verifica se o jogador perdeu o jogo
            elif player.lifes <= 0:
                # Armazena a pontuação
                DATA[fase]['pontuacao'] = player.points
                # Muda o estado do jogo e da fase
                state = 'LOSE'
                running = False
                
            # ----- Gera saídas
            window.blit(assets['background'], (0,0))
            window.blit(player.image, player.rect)
            groups['all_sprites'].draw(window)
            draw_infos(window, assets, player)
            window.blit(pause_button.image, pause_button.rect)

        # Depois de desenhar tudo, atualiza o display.
            pygame.display.update()

        return DATA, state, fase
    else:
        return DATA, 'INIT', fase