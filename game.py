# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from sprites import *
from cenarios import *
from parameters import *

pygame.init()

# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()
FPS = 30

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT)) # SIZE da tela
pygame.display.set_caption('The lost colors') # título da tela

# ----- Importando imagens
background_img = pygame.image.load('assets/img/cidade.png')
background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))

player1_img = pygame.image.load('assets/img/player.png')
player1_img = pygame.transform.scale(player1_img, (SIZE, SIZE*1.5))

chao_img = pygame.image.load('assets/img/chao.png')
chao_img = pygame.transform.scale(chao_img, (SIZE,SIZE))

parede_img = pygame.image.load('assets/img/parede.png')
parede_img = pygame.transform.scale(parede_img, (SIZE, SIZE))

monstro_img = pygame.image.load('assets/img/inimigo1.png')
monstro_img = pygame.transform.scale(monstro_img, (SIZE*(5/7), SIZE*(5/7)))

espinhos_img = pygame.image.load('assets/img/espinhos.png')
espinhos_img = pygame.transform.scale(espinhos_img, (SIZE, SIZE*0.5))

player = Character(player1_img)
all_enemys = pygame.sprite.Group()
all_blocks = pygame.sprite.Group()

for i, linha in enumerate(fase1):
    for j, block in enumerate(linha):
        if block != 0:
            posx = SIZE*j - SIZE*3
            posy = SIZE*i - SIZE*1
            if block == 1:
                bloco = Block(chao_img, posx, posy)
                all_blocks.add(bloco)
            elif block == 2:
                bloco = Block(parede_img, posx, posy)  
                all_blocks.add(bloco)
            elif block == 3:
                monstro = Enemy(monstro_img, posx, posy)
                all_enemys.add(monstro)
            elif block == 4:
                espinhos = Block(espinhos_img, posx, posy + SIZE*0.5)
                all_enemys.add(espinhos)

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
                player.speedy = -50
    
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speedx = 0

    player.update()
    all_blocks.update(player)
    all_enemys.update(player)

    collision_player_blocks = pygame.sprite.spritecollide(player, all_blocks, False)
    for bloco in collision_player_blocks:

        if bloco.rect.bottom > player.rect.bottom > bloco.rect.top:
            player.rect.bottom = bloco.rect.top
            player.jump = True
            player.speedy = 0

        if bloco.rect.top < player.rect.top < bloco.rect.bottom:
            player.rect.top = bloco.rect.bottom

        if bloco.rect.centery < player.rect.bottom:
            player.go_right = not (bloco.rect.right > player.rect.right > bloco.rect.left)
            player.go_left = not (bloco.rect.left < player.rect.left < bloco.rect.right)

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_RIGHT]:
        player.speedx = +10 if player.go_right else 0
    elif pressed_keys[pygame.K_LEFT]:
        player.speedx = -10 if player.go_left else 0

    hits = pygame.sprite.spritecollide(player, all_enemys, False)
    if len(hits) != 0:
        player.lifes -= 1
    
    collision_enemy_wall = pygame.sprite.groupcollide(all_enemys, all_blocks, False, False)
    for monstro, blocos in collision_enemy_wall.items():
        bloco = blocos[0]

        if bloco.rect.right > monstro.rect.right > bloco.rect.left:
            monstro.rect.right = bloco.rect.left
            monstro.speedx = -6

        elif bloco.rect.left < monstro.rect.left < bloco.rect.right:
            monstro.rect.left = bloco.rect.right
            monstro.speedx = +6

    if player.lifes <= 0 or player.rect.top > HEIGHT:
        game = False

    # ----- Gera saídas
    window.blit(background_img, (0,0))
    all_blocks.draw(window)
    all_enemys.draw(window)
    window.blit(player.image, player.rect)

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados