# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from sprites import Block, Personagem

pygame.init()

# ----- Gera tela principal
window = pygame.display.set_mode((900, 600)) # tamanho da tela
pygame.display.set_caption('The lost colors') # título da tela

# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()
FPS = 30
WEIGHT= 600

player_img = pygame.image.load('assets/img/player.png')
player_img = pygame.transform.scale(player_img, (150,200))
bloco_img = pygame.image.load('assets/img/bloco.png')
bloco_img = pygame.transform.scale(bloco_img, (70,70))
background_img = pygame.image.load('assets/img/background.png')
background_img = pygame.transform.scale(background_img, (900,600))

player = Personagem(player_img)



all_blocks = pygame.sprite.Group()
for i in range(10):
    bloco = Block(bloco_img, 35+70*i, WEIGHT)
    all_blocks.add(bloco)

print(pygame.sprite.Group.sprites(all_blocks))

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
                player.speedx+=8
            if event.key == pygame.K_RIGHT:
                player.speedx-=8
            if event.key == pygame.K_UP:
                player.speedy+=40

        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player.speedx-=8
            if event.key == pygame.K_RIGHT:
                player.speedx+=8
            if event.key == pygame.K_UP:
                player.speedy-=40

    # ----- Gera saídas
    all_blocks.update(player)
    
    window.blit(background_img, (0,0))
    window.blit(player.image, player.rect)
    all_blocks.draw(window)
    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador


# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados