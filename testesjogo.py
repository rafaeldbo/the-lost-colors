# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from sprites import Block, Personagem

pygame.init()

WIDTH = 840
HEIGHT = 560

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT)) # tamanho da tela
pygame.display.set_caption('The lost colors') # título da tela

# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()
FPS = 30

player_img = pygame.image.load('assets/img/player.png')
player_img = pygame.transform.scale(player_img, (70,105))
bloco_img = pygame.image.load('assets/img/bloco.png')
bloco_img = pygame.transform.scale(bloco_img, (70,70))
background_img = pygame.image.load('assets/img/background.png')
background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))

player = Personagem(player_img)

all_blocks = pygame.sprite.Group()
for i in range(10):
    bloco = Block(bloco_img, 35+70*i, HEIGHT)
    all_blocks.add(bloco)

all_blocks.add(Block(bloco_img, 280, HEIGHT - 70))

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
                player.speedx-=8
            if event.key == pygame.K_RIGHT:
                player.speedx+=8
            if event.key == pygame.K_UP:
                player.jump()

        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_UP:
                player.speedy-=40
            if event.key == pygame.K_LEFT:
                player.speedx = 0
            if event.key == pygame.K_RIGHT:
                player.speedx = 0

    for block in all_blocks:
        block.rect.x -= player.speedx

    hits = pygame.sprite.spritecollide(player, all_blocks, False)
    for hit in hits:
        if player.rect.bottom >= hit.rect.top:
            player.j = False
            player.rect.bottom = hit.rect.top - 1
        if player.rect.right >= hit.rect.left:
            player.rect.bottom = hit.rect.top + 1

    # if len(hits) > 0:
    #     constante = 70
    # else: 
    #     constante = 0

    # ----- Gera saídas
    all_blocks.update()
    player.update()
    
#    bloco.update(player, constante, (HEIGHT - 70))
    window.blit(background_img, (0,0))
    window.blit(player.image, player.rect)
    all_blocks.draw(window)
    window.blit(bloco.image, bloco.rect)
    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

## função para o boneco não escalar:
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