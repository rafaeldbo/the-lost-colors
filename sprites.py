import pygame
from config import *

# Classe do player
class Character(pygame.sprite.Sprite):
    def __init__(self, assets, colors):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Imagens
        self.stopped_image = assets['personagem']
        self.moviment_anim = assets['movimento personagem']
        self.image = self.stopped_image
        self.mask = pygame.mask.from_surface(self.image)

        # Rect
        self.rect = self.image.get_rect()
        self.rect.left = SIZE*7
        self.rect.bottom = HEIGHT - SIZE*2

        # Variáveis da animação do movimento
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = second/4
        self.frame = 0 
        self.last_frame_image = self.stopped_image

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

        # Variáveis do Shoot
        self.last_shoot = pygame.time.get_ticks()
        self.shoot_delay = 500
        
        # Variáveis do Dash
        self.in_dash= False
        self.last_dash = pygame.time.get_ticks()
        self.dash_delay = 4000
        self.dash_duration = frame*3
     
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
        frame_image = self.last_frame_image
        if self.in_moviment:
            now = pygame.time.get_ticks()
            elapsed_ticks = now - self.last_update
            if elapsed_ticks > self.frame_ticks:
                self.last_update = now
                frame_image = self.moviment_anim[self.frame]
                self.frame = self.frame+1 if self.frame < len(self.moviment_anim)-1 else 0

        # Atualiza a imagem do player parado
        # Utiliza a direção para onde ele estava se movendo
        else:
            frame_image = self.stopped_image
        self.last_frame_image = frame_image

        if self.direction == 'right':
            self.image = frame_image
        elif self.direction == 'left':
            self.image = pygame.transform.flip(frame_image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    # Atualiza a imagem do player com base nas cores coletadas
    def update_color(self, assets):
        self.stopped_image = assets['personagem']
        self.moviment_anim = assets['movimento personagem']

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
        
class Block(pygame.sprite.Sprite):
    def __init__(self, assets, posx, posy, nome):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.name = nome

        # Imagem e rect
        self.image = assets[nome]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy

        self.speedx = 0

    # Atualiza a posição do bloco
    def update(self,player):
        self.speedx = -player.speedx
        self.rect.x += self.speedx
    
    # Atualiza a cor do bloco se o player coletar um novo diamante
    def update_color(self, assets):
        self.image = assets[self.name]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, assets, posx, posy, nome, moviment):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.name = nome

        # Imagem e rect
        self.image = assets[nome]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy + 20

        # Guarda a direção de movimento
        # A direção de movimento é alterada se o inimigo colidir com um bloco
        self.direction = moviment
        self.speed = moviment_enemy

    # Atualiza posição 
    def update(self, player):
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
        self.rect.x -= player.speedx 
    
    # Atualiza cor se o player coletar um novo diamante
    def update_color(self, assets):
        self.image = assets[self.name]

class FireBall(pygame.sprite.Sprite):
    def __init__(self, assets, posx, posy, direction):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Imagem e rect
        image = assets['bola de fogo']
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.centerx = posx 
        self.rect.centery = posy - 60
        
        # Determina a velocidade e imagem da bola de fogo, elas dependem 
        # da direção para a qual o player está se movendo
        if direction == 'right':
            self.speedx = moviment_fireball
            self.image = image
        elif direction == 'left':
            self.speedx = -moviment_fireball
            self.image = pygame.transform.flip(image, True, False)

    # Atualiza posição 
    def update(self, player):
        self.rect.x += self.speedx -player.speedx        

class Collectable(pygame.sprite.Sprite):
    def __init__(self, assets, posx, posy, nome, **kargs):
        # Construtor da classe(Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.name = nome

        self.index = kargs.get('index') # Coleta o index do coletável
        self.color = kargs.get('prism') # coleta a cor (caso for um prisma)
        
        if 'prisma' in nome: # Se for um prisma, define a imagem de acordo com a cor
            img = pygame.image.load(f'assets/img/{nome}.png')
            self.image = pygame.transform.scale(img, (50, 50))
            # diamantes são um pouco menores que o normal
        else:
            self.image = assets[nome] # Define a imagem
        self.mask = pygame.mask.from_surface(self.image) # Cria a mascara de colisão
        # posiciona o sprite
        self.rect = self.image.get_rect()
        self.rect.left = posx if self.color == None else posx+10
        self.rect.top = posy if self.color == None else posy+10

        self.speedx = 0

    def update(self, player):
        # Movimenta o sprite junto com o cenário
        self.speedx = -player.speedx
        self.rect.x += self.speedx
    
    def update_color(self, assets):
        if self.name == 'moeda': # Se for moeda, atualiza a cor
            self.image = assets[self.name]
    
class Flag(pygame.sprite.Sprite):
    def __init__(self, assets, posx, posy, nome):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.name = nome

        self.flag_anim = assets[nome] # Extrai as imagens da animação
        self.image = self.flag_anim[0] # Seleciona a primeira imagem da animação para começar
        # Posiciona o sprite
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy

        # Variáveis usadas na animação
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = second/4
        self.frame = 0 

    def update(self, player):
        # Movimenta o sprite junto com o cenário
        self.speedx = -player.speedx
        self.rect.x += self.speedx    

        # Realiza a animação
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update
        if elapsed_ticks > self.frame_ticks: # Espera o tempo mínimo entre um frame e outro
            self.last_update = now
            self.frame = self.frame+1 if self.frame < len(self.flag_anim)-1 else 0
            self.image = self.flag_anim[self.frame] # Altera a imagem exibida
    
    def update_color(self, assets):
        pass # Essa classe não muda de cor

# Classe da animação da explosão
class Explosion(pygame.sprite.Sprite):
    def __init__(self, posx, posy, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.explosion_anim = assets['explosao'] # Extrai as imagens da animação
        self.image = self.explosion_anim[0] # Seleciona a primeira imagem da animação para começar
        # Posiciona o centro da sprite
        self.rect = self.image.get_rect()
        self.rect.centerx = posx  
        self.rect.centery = posy

        # Variáveis usadas na animação
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 50
        self.frame = 0 

    def update(self, player):
        # Movimenta o sprite junto com o cenário
        self.speedx = -player.speedx
        self.rect.x += self.speedx    

        # Realiza a animação
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update
        if elapsed_ticks > self.frame_ticks: # Espera o tempo mínimo entre um frame e outro
            self.last_update = now
            self.frame += 1

            # Verifica se já chegou no final da animação.
            if self.frame == len(self.explosion_anim):
                self.kill() # Termina a animação
            else:
                # Continua a animação
                centerx = self.rect.centerx
                centery = self.rect.centery
                self.image = self.explosion_anim[self.frame]  # Altera a imagem exibida
                self.rect = self.image.get_rect()
                self.rect.centerx = centerx - player.speedx
                self.rect.centery = centery

    def update_color(self, assets):
        pass # Essa classe não muda de cor
