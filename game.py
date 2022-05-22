# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from requests import delete
from sprites import Block, Monstrinho, Personagem
from cenarios import *
from parameters import *

pygame.init()

# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()
FPS = 30
go_front = True
go_back = True
# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT)) # tamanho da tela
pygame.display.set_caption('The lost colors') # título da tela

# ----- Importando imagens
player_img = pygame.image.load('assets/img/player.png')
player_img = pygame.transform.scale(player_img, (70, 105))
background_img = pygame.image.load('assets/img/cidade.png')
background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))

chao_img = pygame.image.load('assets/img/bloco3.png')
chao_img = pygame.transform.scale(chao_img, (70,70))

tijolo_img = pygame.image.load('assets/img/bloco4.png')
tijolo_img = pygame.transform.scale(tijolo_img, (70,70))

monstro_img= pygame.image.load('assets/img/inimigo1.png')
monstro_img = pygame.transform.scale(monstro_img, (50,50))

player = Personagem(player_img)
monstros_varios = pygame.sprite.Group()
all_blocks = pygame.sprite.Group()

for i, linha in enumerate(fase1):
    for j, block in enumerate(linha):
        if block != 0:
            posx = tamanho*j - 210
            posy = tamanho*i - 70
            if block == 1:
                bloco = Block(chao_img, posx, posy)
                all_blocks.add(bloco)
            elif block == 2:
                bloco = Block(tijolo_img, posx, posy)  
                all_blocks.add(bloco)
            elif block == 3:
                monstro = Monstrinho(monstro_img,posx,posy+20)
                monstros_varios.add(monstro)
lifes= 1         

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    collisionx = pygame.sprite.spritecollide(player, all_blocks, False)
    for bloco in collisionx:
        if bloco.rect.right > player.rect.right >= bloco.rect.left and bloco.rect.centery < player.rect.bottom:
            go_front = False
        if bloco.rect.left < player.rect.left <= bloco.rect.right and bloco.rect.centery < player.rect.bottom:
            go_back = False
    
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_LEFT] and go_back:
        player.speedx = -10
    elif pressed_keys[pygame.K_LEFT] and not go_back:
        player.speedx = 0
    if pressed_keys[pygame.K_RIGHT] and go_front:
        player.speedx = +10
    elif pressed_keys[pygame.K_RIGHT] and not go_front:
        player.speedx = 0

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT: 
            game = False

        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP and player.jump:
                player.jump = False
                player.speedy = -60
    
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speedx = 0

    print(go_back, go_front)
    player.update()
    collision = pygame.sprite.spritecollide(player, all_blocks, False)

    for bloco in collision:
        if player.rect.bottom >= bloco.rect.top and player.rect.bottom <= bloco.rect.bottom:
            player.rect.bottom = bloco.rect.top
            player.jump = 2
            player.speedy = 0
        if player.rect.top <= bloco.rect.bottom and player.rect.top >= bloco.rect.top:
            player.rect.top = bloco.rect.bottom
        
        
    collision2 = pygame.sprite.spritecollide(player, monstros_varios, False)
    for monstro in collision2:
        if player.rect.bottom >= monstro.rect.top and player.rect.bottom <= monstro.rect.bottom:
            lifes-=1
        elif player.rect.top <= monstro.rect.bottom and player.rect.top >= monstro.rect.top:
            lifes-=1
        elif player.rect.right >= monstro.rect.left and player.rect.right <= monstro.rect.left:
            lifes-=1
        elif player.rect.left >= monstro.rect.right and player.rect.left <= monstro.rect.right:
            lifes-=1
        
    
    collision_group = pygame.sprite.groupcollide(monstros_varios, all_blocks, False, False)
    for monstro, blocos in collision_group.items():
        bloco = blocos[0]

        if bloco.rect.right > monstro.rect.right > bloco.rect.left:
            monstro.rect.right = bloco.rect.left
            monstro.speedx = -6

        elif bloco.rect.left < monstro.rect.left < bloco.rect.right:
            monstro.rect.left = bloco.rect.right
            monstro.speedx = +6

    if lifes == 0 or player.rect.top > HEIGHT:
        game=False

    all_blocks.update(player)
    monstros_varios.update(player)
    # ----- Gera saídas
    window.blit(background_img, (0,0))
    window.blit(player.image, player.rect)
    all_blocks.draw(window)
    monstros_varios.draw(window)
    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador
    go_front = True
    go_back = True

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados