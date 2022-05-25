# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from sprites import *
from cenarios import * 
from parameters import *
from assets import assets, groups

pygame.init()

# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()
FPS = 30

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT)) # SIZE da tela
pygame.display.set_caption('The lost colors') # título da tela

player = Character(assets['player'])

def fica_no_bloco (player, bloco):
    minimo = (player.rect.right - player.rect.centerx)/2
    if player.rect.right > bloco.rect.left and player.rect.left < bloco.rect.left:
        if (player.rect.right - bloco.rect.left) > minimo:
            return True
    elif player.rect.right > bloco.rect.right and player.rect.left < bloco.rect.right:
        if (bloco.rect.right - player.rect.left) > minimo:
            return True
    elif player.rect.centerx > bloco.rect.left:
        return True
    return False

for i, linha in enumerate(fase1):
    for j, block in enumerate(linha):
        if block != "0":
            posx = SIZE*j - SIZE*3
            posy = SIZE*i - SIZE*1
            if block == "c":
                bloco = Block(assets['chao'], posx, posy)
                groups['all_blocks'].add(bloco)
            elif block == "p":
                bloco = Block(assets['parede'], posx, posy)  
                groups['all_blocks'].add(bloco)
            elif block == "i":
                monstro = Enemy(assets['monstro'], posx, posy)
                groups['all_enemys'].add(monstro)
            elif block == "e":
                espinhos = Block(assets['espinhos'], posx, posy + SIZE/2)
                groups['all_enemys'].add(espinhos)
            elif block == "d":
                diamante = Diamonds(assets['diamante'], posx, posy)
                groups['diamond'].add(diamante)
            elif block == "m":
                coin = Coin(assets['coin'], posx, posy)
                groups['coins'].add(coin)

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            game = False

        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player.jump:
                player.jump = False
                player.speedy = -moviment_player_y
            if event.key == pygame.K_SPACE:
                player.shoot(assets['bola de fogo'], groups['all_fireballs'])
    
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speedx = 0

    player.update()
    groups['all_fireballs'].update(player)
    groups['all_blocks'].update(player)
    groups['all_enemys'].update(player)
    groups['diamond'].update(player)
    groups['coins'].update(player)

    collision_player_diamond = pygame.sprite.spritecollide(player, groups['diamond'], True, pygame.sprite.collide_mask)
    if len(collision_player_diamond) != 0:
        player.fireballs = True

    collision_player_blocks = pygame.sprite.spritecollide(player, groups['all_blocks'], False)
    for bloco in collision_player_blocks:

        if bloco.rect.bottom > player.rect.bottom > bloco.rect.top:
            ficaNoBloco = fica_no_bloco(player,bloco)
            if ficaNoBloco:
                player.rect.bottom = bloco.rect.top
            player.jump = True
            player.speedy = 0

        if bloco.rect.top < player.rect.top < bloco.rect.bottom:
            player.rect.top = bloco.rect.bottom

        if bloco.rect.centery < player.rect.bottom and not lado:
            player.go_right = not (bloco.rect.right > player.rect.right > bloco.rect.left)
            player.go_left = not (bloco.rect.left < player.rect.left < bloco.rect.right)

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_RIGHT]:
        player.speedx = +moviment_player_x if player.go_right else 0
    elif pressed_keys[pygame.K_LEFT]:
        player.speedx = -moviment_player_x if player.go_left else 0

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

    collision_enemy_fireball = pygame.sprite.groupcollide(groups['all_enemys'], groups['all_fireballs'], True, True, pygame.sprite.collide_mask)
    player.points += 100*len(collision_enemy_fireball)
    collision_blocos_fireball = pygame.sprite.groupcollide(groups['all_blocks'], groups['all_fireballs'], False, True)

    collision_player_coin = pygame.sprite.spritecollide(player, groups['coins'], True, pygame.sprite.collide_mask)
    player.points += 100*len(collision_player_coin)

    if player.lifes <= 0 or player.rect.top > HEIGHT:
        game = False

    # ----- Gera saídas
    window.blit(assets['background'], (0,0))
    groups['all_blocks'].draw(window)
    groups['all_enemys'].draw(window)
    groups['all_fireballs'].draw(window)
    groups['diamond'].draw(window)
    groups['coins'].draw(window)
    window.blit(player.image, player.rect)

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador
    
# ===== Finalização =====
print(player.points)
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados