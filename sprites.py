import pygame
from config import *
from assets import load_assets

class Entity(pygame.sprite.Sprite):
    def __init__(self, assets, name, position, animation=False):
        # "animation" recebe a quantidade de frames por segundo que a animação possui

        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.name = name

        # Imagem
        self.image = assets[name]
        
        self.animated = False
        if animation:
            self.animated = True
            self.animation = assets[f"animacao {name}"]
            # Variáveis usadas na animação
            self.last_update = pygame.time.get_ticks()
            self.frame_ticks = second/animation
            self.frame = 0 

        # Mascara
        self.mask = pygame.mask.from_surface(self.image)

        # Rect
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position

        # Variaveis de Movimento
        self.speedx = 0

    def update(self, player):
        # Movimenta o sprite junto com o cenário (movimento relativo ao player)
        self.speedx = -player.speedx
        self.rect.x += self.speedx

        # Atualiza a animação
        if self.animated:
            self.image = self.update_animation() # Altera a imagem exibida

    def update_animation(self):
        # Realiza a animação
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update
        if elapsed_ticks > self.frame_ticks: # Espera o tempo mínimo entre um frame e outro
            self.last_update = now
            self.frame = self.frame+1 if self.frame < len(self.animation)-1 else 0 # Atualiza o frame
        frame_image = self.animation[self.frame] # Altera a imagem exibida
        return frame_image
    
    def update_color(self, assets):
        self.image = assets[self.name]
        if self.animated:
            self.animation = assets[f'animacao {self.name}']

# Classe do player
class Character(Entity):
    def __init__(self, assets, colors):
        # Inicializando entidade do personagem
        Entity.__init__(self, assets, 'personagem', (SIZE*7, SIZE*8-SIZE*1.5), animation=4)

        # Imagens
        self.stopped_image = self.image

        # Variáveis do Movimento
        self.speedx = 0
        self.speedy = gravidade
        self.direction = 'right'
        self.in_moviment = True
        self.jump = 0

        # Variáveis do personagem
        self.lifes = 3
        self.colors = colors
        self.points = 0
        self.collected = []
        self.checkpoint = 0

        # Variáveis do Shoot
        self.last_shoot = pygame.time.get_ticks()
        self.shoot_delay = 500
        
        # Variáveis do Dash
        self.in_dash= False
        self.last_dash = pygame.time.get_ticks()
        self.dash_delay = 4000
        self.dash_duration = frame*3
     
    # Realiza movimento e animação
    # Override
    def update(self):
        # Verifica a velocidade no eixo y
        self.speedy += 0 if self.speedy >= gravidade*4 else gravidade
        # Atualiza posição
        self.rect.y += self.speedy

        # Colisão com o teto do jogo, coloca o player dentro da tela
        if self.rect.y < 0:
            self.rect.y == 0
            self.speedy = 0
        
        self.in_moviment = (self.speedx != 0)
        # Define a direção do personagem
        if self.speedx > 0:
            self.direction = 'right'
        elif self.speedx < 0:
            self.direction = 'left'
        
        # Animação do personagem em movimento, atualiza a imagem
        if self.in_moviment:
            frame_image = self.update_animation()
        else:
            frame_image = self.stopped_image # Atualiza a imagem do player parado

        if self.direction == 'right':
            self.image = frame_image
        elif self.direction == 'left':
            self.image = pygame.transform.flip(frame_image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    # Atualiza a imagem do player com base nas cores coletadas
    # Override
    def update_color(self, assets):
        super().update_color(assets)
        self.stopped_image = self.image

    # Atira bola de fogo
    def shoot (self, img, groups):
        if "red" in self.colors:
            now = pygame.time.get_ticks()
            # Controla se o player pode ou não atirar 
            # Dependendo do tempo decorrido desde o último tiro
            elapsed_ticks = now - self.last_shoot
            if elapsed_ticks > self.shoot_delay:
                self.last_shoot = now
                # Cria a bola de fogo
                fireball = FireBall(img, self.rect.centerx, self.rect.bottom, self.direction)
                groups['all_fireballs'].add(fireball)
                groups['all_sprites'].add(fireball)

    # Função do dash
    def dash(self, assets):
        # Só tem o poder do dash se tiver coletado o diamante verde
        if "green" in self.colors:
            now = pygame.time.get_ticks()
            # Controla se o player pode ou não dar dash
            # Dependendo do tempo decorrido desde o último dash
            elapsed_ticks = now - self.last_dash
            if elapsed_ticks > self.dash_delay and not self.in_dash:
                assets['dash som'].play()
                self.last_dash = now
                # altera a velocidade do movimento em x
                if self.direction == 'right':
                    self.speedx = +65
                elif self.direction == 'left':
                    self.speedx = -65
                self.in_dash = True      

class Button(pygame.sprite.Sprite):
    def __init__(self, rect, value, **kargs):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = kargs.get('image')
        self.rect = pygame.Rect(rect)
        self.value = value
        
class Block(Entity):
    def __init__(self, assets, posx, posy, name):
        # Inicializando entidade
        Entity.__init__(self, assets, name, (posx, posy))

class Enemy(Entity):
    def __init__(self, assets, posx, posy, name, moviment):
        # Inicializando entidade
        Entity.__init__(self, assets, name, (posx, posy+20))

        # Guarda a direção de movimento
        # A direção de movimento é alterada se o inimigo colidir com um bloco
        self.direction = moviment
        self.speed = moviment_enemy

    # Realiza movimento
    # Override 
    def update(self, player):
        super().update(player)
        if self.direction == "horizontal":
            self.rect.x += self.speed
        if self.direction == "vertical":
            self.rect.y += self.speed
            # Mantém o robô dentro da tela
            if self.rect.top < 0:
                self.rect.top = 0
                self.speed = -self.speed
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
                self.speed = -self.speed

class FireBall(Entity):
    def __init__(self, assets, posx, posy, direction):
        # Inicializando entidade
        adjust_x = -SIZE if direction == 'left' else 0
        Entity.__init__(self, assets, 'bola de fogo', (posx+adjust_x, posy-SIZE*1.25))
        
        # Determina a velocidade e imagem da bola de fogo, elas dependem 
        # da direção para a qual o player está se movendo
        if direction == 'right':
            self.speed = moviment_fireball
        elif direction == 'left':
            self.speed = -moviment_fireball
            self.image = pygame.transform.flip(self.image, True, False)

    # Realiza movimento
    # Override
    def update(self, player):
        super().update(player)
        self.rect.x += self.speed       

class Collectable(Entity):
    def __init__(self, assets, posx, posy, name, index, animation=False):
        # Inicializando entidade
        Entity.__init__(self, assets, name, (posx, posy), animation=animation)

        self.index = index # Coleta o index do coletável

class Coin(Collectable):
    def __init__(self, assets, posx, posy, name, index):
        # Inicializando entidade
        Collectable.__init__(self, assets, posx, posy, name, index)

class Checkpoint(Collectable):
    def __init__(self, assets, posx, posy, name, index, animation=False):
        # Inicializando entidade
        Collectable.__init__(self, assets, posx, posy, name, index, animation=animation)

class Flag(Checkpoint):
    def __init__(self, assets, posx, posy, name, index):
        # Inicializando entidade
        Checkpoint.__init__(self, assets, posx, posy, name, index, animation=4)

class Prism(Checkpoint):
    def __init__(self, assets, posx, posy, name, color, index, animation=False):
        # Inicializando entidade
        Checkpoint.__init__(self, assets, posx, posy, name, index, animation=animation)
                
        self.color = color # Cor do prisma
    
    # Atualiza os assets com a nova cor
    def update_assets_color(self, assets, fase, player):
        player.colors.append(self.color)
        assets = load_assets(fase, player.colors)
        player.update_color(assets)

        return assets, player
    
# Classe da animação da explosão
class Explosion(Entity):
    def __init__(self, posx, posy, assets):
        # Inicializando entidade
        Entity.__init__(self, assets, 'explosao', (posx-SIZE/2, posy-SIZE/2), animation=20)

    # Finalizando a animação
    # Override
    def update(self, player):
        super().update(player)
        # Verifica se já chegou no final da animação.
        if self.frame == len(self.animation)-1:
            self.kill() # Termina a animação