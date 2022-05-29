# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from parameters import *
from functions import * 
from sprites import *
from assets import *

pygame.init()
assets = load_assets()
init= True
game1= False
end= False
clock = pygame.time.Clock()
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT)) # SIZE da tela
pygame.display.set_caption('The lost colors') # título da tela

while init:
    clock.tick(FPS)
    # ----- Trata eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            init = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                init = False
                game1= True
            
    window.blit(assets['background'], (0,0))
    pygame.display.flip()

groups = load_map('fase1', assets)
player = Character(assets['personagem'])

# ===== Loop principal =====
while game1:
    clock.tick(FPS)

    if player.in_dash:
        now = pygame.time.get_ticks()
        elapsed_ticks = now - player.last_dash
        if elapsed_ticks >= 100:
            player.speedx = 0
            player.in_dash = False
        

    # ----- Trata eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            game1 = False
        
        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player.jump:
                player.jump = False
                player.speedy = -moviment_player_y
            if event.key == pygame.K_SPACE:
                player.shoot(assets['bola de fogo'], groups)
            if event.key == pygame.K_z:
                player.dash()
                    
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speedx = 0
        

    player.update()
    groups['all_sprites'].update(player)

    nearby_blocks = []
    for block in groups['all_blocks']:
        if (block.rect.left >= (player.rect.left - SIZE) or block.rect.left <= (player.rect.right + SIZE)) and (block.rect.top >= (player.rect.top - SIZE) or (block.rect.bottom <= player.rect.bottom + SIZE)):
            nearby_blocks.append(block)
    collision_player_blocks = pygame.sprite.spritecollide(player, nearby_blocks, False)
    for bloco in collision_player_blocks:

        if bloco.rect.top < player.rect.top < bloco.rect.bottom and colisao_minima(player, bloco): # Colisão com o teto
            player.rect.top = bloco.rect.bottom

        if bloco.rect.bottom > player.rect.bottom > bloco.rect.top and colisao_minima(player, bloco): # Colisão com o chão
            player.rect.bottom = bloco.rect.top
            player.jump = True
            player.speedy = 0

        if bloco.rect.bottom < (player.rect.bottom + (SIZE/8)) and bloco.rect.bottom > (player.rect.top + (SIZE/8)): # Colisão com as laterais
            player.go_right = not (bloco.rect.right > player.rect.right > bloco.rect.left)
            player.go_left = not (bloco.rect.left < player.rect.left < bloco.rect.right)

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_RIGHT]:
        player.speedx = +moviment_player_x if player.go_right else 0
    elif pressed_keys[pygame.K_LEFT]:
        player.speedx = -moviment_player_x if player.go_left else 0
    
    if not player.in_dash:
        hits = pygame.sprite.spritecollide(player, groups['all_enemys'], False, pygame.sprite.collide_mask)
        if len(hits) != 0:
            player.lifes -= 1
    
    collision_enemy_blocks = pygame.sprite.groupcollide(groups['all_enemys'], groups['all_blocks'], False, False)
    for monstro, blocos in collision_enemy_blocks.items():
        bloco = blocos[0]

        if bloco.rect.right > monstro.rect.right > bloco.rect.left:
            monstro.rect.right = bloco.rect.left
            monstro.speedx = -moviment_enemy_x

        elif bloco.rect.left < monstro.rect.left < bloco.rect.right:
            monstro.rect.left = bloco.rect.right
            monstro.speedx = +moviment_enemy_x

    # Colisões da bola de fogo
    collision_enemy_fireball = pygame.sprite.groupcollide(groups['all_enemys'], groups['all_fireballs'], True, True, pygame.sprite.collide_mask)
    player.points += 100*len(collision_enemy_fireball)

    collision_blocos_fireball = pygame.sprite.groupcollide(groups['all_blocks'], groups['all_fireballs'], False, True)

    # Colisões com as moedas e diamantes (coletáveis)
    collision_player_collectibles = pygame.sprite.spritecollide(player, groups['collectibles'], True, pygame.sprite.collide_mask)
    for collected in collision_player_collectibles:
        player.points += 100
        if collected.color != None:
            player.colors.append(collected.color)
            assets = load_assets(colors=player.colors)
            player.update_color(assets)
            for entity in groups['all_sprites']:
                entity.update_color(assets)

    # Verifica se o jogador perdeu o jogo
    if player.lifes <= 0 or player.rect.top > HEIGHT:
        game1 = False
        end = True

    # ----- Gera saídas
    window.blit(assets['background'], (0,0))
    window.blit(player.image, player.rect)
    groups['all_sprites'].draw(window)

    pygame.display.update()

while end:
    clock.tick(FPS)
    # ----- Trata eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            end = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game1= True
            if event.key == pygame.K_ESCAPE:
                end= False
    window.blit(assets['background'], (0,0))
    pygame.display.flip()



# ===== Finalização =====
print(player.points)
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados