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

    for block in groups['all_blocks']:
        if (block.rect.left >= (player.rect.left - SIZE) or block.rect.right <= (player.rect.right + SIZE)) and (block.rect.top >= (player.rect.top - SIZE) or (block.rect.bottom <= player.rect.bottom + SIZE)):
            nearby_blocks.append(block)
            if (block.rect.centery > player.rect.top and block.rect.centery < player.rect.bottom):
                if block.rect.right <= player.rect.left:
                    vmin_esquerda = block.rect.right - player.rect.left
                if block.rect.left >= player.rect.right:
                    vmax_direita = block.rect.left - player.rect.right

        pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_RIGHT]:
        player.speedx = +moviment_player_x if (vmax_direita >= moviment_player_x) else (+vmax_direita)
    elif pressed_keys[pygame.K_LEFT]:
        player.speedx = -moviment_player_x if (-moviment_player_x >= vmin_esquerda) else (-vmin_esquerda)

                for element in collision_breakables_fireballs:
                assets['explode som'].play()
                explosao = Explosion(element.rect.centerx, element.rect.centery, assets)
                groups['all_sprites'].add(explosao)
                
class Explosion(pygame.sprite.Sprite):
    def __init__(self, posx, posy, assets):
        
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação de explosão
        self.explosion_anim = assets['explosao']

        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0  # Armazena o índice atual na animação
        self.image = self.explosion_anim[self.frame]  # Pega a primeira imagem
        self.rect = self.image.get_rect()
        self.rect.centerx = posx  # Posiciona o centro da imagem
        self.rect.centery = posy

        # Guarda o tick da primeira imagem, ou seja, o momento em que a imagem foi mostrada
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        # Quando pygame.time.get_ticks() - self.last_update > self.frame_ticks a
        # próxima imagem da animação será mostrada
        self.frame_ticks = 50

    def update(self, player):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Verifica se já chegou no final da animação.
            if self.frame == len(self.explosion_anim):
                # Se sim, tchau explosão!
                self.kill()
            else:
                # Se ainda não chegou ao fim da explosão, troca de imagem.
                centerx = self.rect.centerx
                centery = self.rect.centery
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.centerx = centerx - player.speedx
                self.rect.centery = centery