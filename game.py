# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from sprites import Block, Personagem
from cenarios import *
from parameters import *

pygame.init()

# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()
FPS = 60

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

player = Personagem(player_img)

all_blocks = pygame.sprite.Group()
for i, linha in enumerate(fase1):
    for j, block in enumerate(linha):
        if block != 0:
            posx = tamanho*j - 210
            posy = tamanho*i - 70
            if block == 1:
                bloco = Block(chao_img, posx, posy)
            elif block == 2:
                bloco = Block(tijolo_img, posx, posy)  
            all_blocks.add(bloco)

# ===== Loop principal =====
while game:
    clock.tick(FPS)
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT: 
            game = False

        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                player.speedx = -10
            if event.key == pygame.K_RIGHT:
                player.speedx = +10
            if event.key == pygame.K_UP and player.jump:
                player.jump = False
                player.speedy = -60

        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speedx = 0
    
    player.update()

    hits = pygame.sprite.spritecollide(player, all_blocks, False)
    for bloco in hits:
        if bloco.rect.top < player.rect.top < bloco.rect.bottom:
            player.rect.top = bloco.rect.bottom

        if bloco.rect.bottom > player.rect.bottom > bloco.rect.top:
            player.rect.bottom = bloco.rect.top
            player.jump = 2
            player.speedy = 0
        
        if player.rect.bottom >= bloco.rect.bottom:
            if bloco.rect.right > player.rect.right > bloco.rect.left and player.speedx > 0:
                player.speedx = 0
            if bloco.rect.left > player.rect.left < bloco.rect.right and player.speedx < 0:
                player.speedx = 0

    all_blocks.update(player)

    if player.rect.top > HEIGHT:
        game = False

    # ----- Gera saídas
    window.blit(background_img, (0,0))
    window.blit(player.image, player.rect)
    all_blocks.draw(window)
    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados