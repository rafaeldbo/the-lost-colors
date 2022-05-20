# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from sprites import Block, Personagem
from cenarios import fase1

pygame.init()

gravidade = 10
WIDTH = 840
HEIGHT = 560

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT)) # tamanho da tela
pygame.display.set_caption('The lost colors') # título da tela

# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()
FPS = 30
tamanho = 70

player_img = pygame.image.load('assets/img/player.png')
player_img = pygame.transform.scale(player_img, (70,105))
bloco_img = pygame.image.load('assets/img/bloco.png')
bloco_img = pygame.transform.scale(bloco_img, (70,70))
background_img = pygame.image.load('assets/img/cidade.png')
background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))

player = Personagem(player_img)

all_blocks = pygame.sprite.Group()
for i, linha in enumerate(fase1):
    for j, block in enumerate(linha):
        if block == 1:
            bloco = Block(bloco_img, tamanho*j, tamanho*i)
            all_blocks.add(bloco)

# ===== Loop principal =====
while game:
    clock.tick(FPS)
    # ----- Trata eventos
    for event in pygame.event.get(): # py.game.event.get() armazena ações do jogo e do usuário
        # ----- Verifica consequências
        if event.type == pygame.QUIT: 
            game = False
        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player.speedx = +8
            if event.key == pygame.K_RIGHT:
                player.speedx = -8
            if event.key == pygame.K_UP and player.jump:
                player.jump = False
                player.speedy = -60

        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speedx = 0


    player.update()

    collision = pygame.sprite.spritecollide(player, all_blocks, False)
    hitsx = []

    for bloco in collision:
        if player.rect.bottom >= bloco.rect.top and player.rect.bottom < bloco.rect.bottom:
            player.rect.bottom = bloco.rect.top
            player.jump = True
            player.speedy = 0
        if player.rect.top <= bloco.rect.bottom and player.rect.top > bloco.rect.top:
            player.rect.top = bloco.rect.bottom

    all_blocks.update(player)

    # ----- Gera saídas
    window.blit(background_img, (0,0))
    window.blit(player.image, player.rect)
    all_blocks.draw(window)
    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador


# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados