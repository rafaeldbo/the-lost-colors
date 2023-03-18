import pygame
from config import *
from assets import load_assets

class Button(pygame.sprite.Sprite):
    def __init__(self, rect, value, image=None):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = pygame.Rect(rect)

        self.value = value

class Entity(pygame.sprite.Sprite):
    # "animation" recebe a quantidade de frames por segundo que a animação possui
    def __init__(self, assets, name, position, speed=(0,0), animation=False):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.name = name

        # Imagens
        self.image = assets[name]
        
        self.animated = bool(animation)
        if self.animated:
            self.animation = assets[f"animacao {name}"]
            # Variáveis usadas na animação
            self.last_update = pygame.time.get_ticks()
            self.frame_ticks = SECOND/animation
            self.frame = 0 

        # Mascara
        self.mask = pygame.mask.from_surface(self.image)

        # Rect
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position

        # Variaveis de Movimento
        self.speedx, self.speedy = speed
    
    def delay(self, delay, last):
        # Verifica se terminou o delay da ação
        now = pygame.time.get_ticks()
        elapsed_ticks = now - last
        if elapsed_ticks > delay:
            return True, now
        return False, last
        
    def moviment(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # Mantém a entidade dentro da tela
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speedy = -self.speedy
            
            self.rect.top = 0 if self.rect.top < 0 else self.rect.top
            self.rect.bottom = 0 if self.rect.bottom > HEIGHT else self.rect.bottom

    def update(self, player):
        # Movimenta o sprite junto com o cenário (movimento relativo ao player)
        self.rect.x += -player.speedx
        self.moviment()

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
        # Inicializando classe mãe
        Entity.__init__(self, assets, 'personagem', (SIZE*7, SIZE*8-SIZE*1.5), animation=4)

        # Imagens
        self.stopped_image = self.image

        # Variáveis do Movimento
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
        
        # Variáveis do Dash
        self.in_dash= False
        self.last_dash = pygame.time.get_ticks()
     
    # Realiza movimento e animação
    # Override
    def update(self):
        # Movimento em y do player pela gravidade
        self.speedy += 0 if self.speedy >= GRAVIDADE*4 else GRAVIDADE
        self.rect.y += self.speedy

        # Impede o player de atravessar o teto
        if self.rect.y < 0:
            self.rect.y = 0
            self.speedy = 0
        
        # Verifica se está em movimento
        self.in_moviment = (self.speedx != 0)

        # Define a direção do personagem
        if self.in_moviment:
            self.direction = 'right' if self.speedx > 0 else "left"
        
        # Atualiza imagem do personagem: animação de movimento ou parado
        frame_image = self.update_animation() if self.in_moviment else self.stopped_image
        self.image = frame_image if self.direction == 'right' else pygame.transform.flip(frame_image, True, False)

        # Atualiza a mascara do player
        self.mask = pygame.mask.from_surface(self.image)

    # Atualiza a imagem do player com base nas cores coletadas
    # Override
    def update_color(self, assets):
        super().update_color(assets)
        self.stopped_image = self.image

    # Função do dash
    def dash(self, assets):
        # Só tem o poder do dash se tiver coletado o diamante verde
        if "green" in self.colors:
            # Controla se o player pode ou não dar dash
            # Dependendo do tempo decorrido desde o último dash
            dash, self.last_dash = self.delay(DASH_DELAY, self.last_dash)
            if dash:
                # altera a velocidade do movimento em x
                self.speedx = DASH_SPEED*DIRECTION[self.direction]
                assets['dash som'].play()  
                self.in_dash = True

    # Atira bola de fogo
    def shoot (self, img, groups):
        # Só tem o poder do dash se tiver coletado o diamante vermelho
        if "red" in self.colors:
            # Controla se o player pode ou não atirar 
            # Dependendo do tempo decorrido desde o último tiro
            shoot, self.last_shoot = self.delay(SHOOT_DELAY, self.last_shoot)
            if shoot:
                # Cria a bola de fogo
                fireball = FireBall(img, self.rect.centerx, self.rect.centery, self.direction)
                groups['fireballs'].add(fireball)
                groups['all_sprites'].add(fireball)
        
class Block(Entity):
    def __init__(self, assets, name, position):
        # Inicializando classe mãe
        Entity.__init__(self, assets, name, position)

class Enemy(Entity):
    def __init__(self, assets, name, position, speed):
        # Inicializando classe mãe
        Entity.__init__(self, assets, name, position, speed)

class FireBall(Entity):
    def __init__(self, assets, posx, posy, direction):
        # Inicializando classe mãe
        Entity.__init__(self, assets, 'bola de fogo', (posx+(SIZE*DIRECTION[direction])/2, posy-SIZE/2), (FIREBALL_SPEED*DIRECTION[direction], 0))
  
        if direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)   

class Collectable(Entity):
    def __init__(self, assets, name, position, index, animation=False):
        # Inicializando classe mãe
        Entity.__init__(self, assets, name, position, animation=animation)

        self.index = index # Coleta o index do coletável

class Coin(Collectable):
    def __init__(self, assets, name, position, index):
        # Inicializando classe mãe
        Collectable.__init__(self, assets, name, position, index)

class Checkpoint(Collectable):
    def __init__(self, assets, name, position, index, animation=False):
        # Inicializando classe mãe
        Collectable.__init__(self, assets, name, position, index, animation=animation)

class Flag(Checkpoint):
    def __init__(self, assets, name, position, index):
        # Inicializando classe mãe
        Checkpoint.__init__(self, assets, name, position, index, animation=4)

class Prism(Checkpoint):
    def __init__(self, assets, name, position, index, color):
        # Inicializando classe mãe
        Checkpoint.__init__(self, assets, name, position, index)
                
        self.color = color # Cor do prisma
    
    # Atualiza os assets com a nova cor
    def update_assets_color(self, assets, player, fase):
        player.colors.append(self.color)
        assets = load_assets(fase, player.colors)
        player.update_color(assets)

        return assets, player
    
# Classe da animação da explosão
class Explosion(Entity):
    def __init__(self, assets, posx, posy):
        # Inicializando classe mãe
        Entity.__init__(self, assets, 'explosao', (posx-SIZE/2, posy-SIZE/2), animation=20)

        assets['explode som'].play()

    # Finalizando a animação
    # Override
    def update(self, player):
        super().update(player)
        # Verifica se já chegou no final da animação.
        if self.frame == len(self.animation)-1:
            self.kill() # Termina a animação