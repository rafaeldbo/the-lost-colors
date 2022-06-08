import json, io
from config import *
from sprites import *

def load_matriz(fase):
    with open(f'assets/{fase}.csv', 'r') as arquivo:
        fase_lines = arquivo.readlines()
    separator = fase_lines[1][1]
    colunas = {}

    for linha in fase_lines:
        linha = linha.strip()
        linha = linha.split(separator)
        for i, value in enumerate(linha):
            if i not in colunas.keys():
                colunas[i] = [value]
            elif i in colunas.keys():
                colunas[i].append(value)
    
    matriz_fase = []
    for j in colunas.keys():
        coluna = colunas[j]
        matriz_fase.append(coluna)

    return matriz_fase
    
def load_map(matriz_fase, assets, checkpoint, current_colors, **kargs):

    groups = {
        'all_blocks': pygame.sprite.Group(), # Todos os Blocos {possuem colisão}
        'all_monsters': pygame.sprite.Group(), # Todas os Monstros (possuem movimento)
        'all_fireballs': pygame.sprite.Group(), # Tadas as Bolas de fogo (destruem entidades)
        'collectibles': pygame.sprite.Group(), # Todas as Entidades Coletaveis
        'breakables': pygame.sprite.Group(), # Todas as Entidades Quebraveis com Bola de Fogo
        'damagers': pygame.sprite.Group(), # Todas as Entidade que causam Dano
        'all_sprites': pygame.sprite.Group(), # Todas as Entidades
    }

    collected = kargs.get('collected') if kargs.get('collected') != None else []

    for j, coluna in enumerate(matriz_fase):
        if j in range(checkpoint['inicio'], checkpoint['fim']):
            for i, value in enumerate(coluna):
                
                if value != "0":
                    posx = SIZE*j - checkpoint['parede'] - checkpoint['inicio']*SIZE
                    posy = SIZE*i

                    if value == "c":
                        element = Block(assets, posx, posy, "chao")
                        groups['all_blocks'].add(element)
                        groups['all_sprites'].add(element)

                    elif value == "p":
                        element = Block(assets, posx, posy, "parede")
                        groups['all_blocks'].add(element)
                        groups['all_sprites'].add(element)

                    elif value == "i1":
                        element = Enemy(assets, posx, posy, "inimigo chao", "horizontal")
                        groups['all_monsters'].add(element)
                        groups['damagers'].add(element)
                        groups['breakables'].add(element)
                        groups['all_sprites'].add(element)

                    elif value == "i2":
                        element = Enemy(assets, posx, posy, "inimigo chao", "vertical")
                        groups['all_monsters'].add(element)
                        groups['damagers'].add(element)
                        groups['breakables'].add(element)
                        groups['all_sprites'].add(element)

                    elif value == "e":
                        element = Block(assets, posx, posy, "espinhos")
                        groups['damagers'].add(element)
                        groups['all_sprites'].add(element)
                
                    elif value == "q":
                        element = Block(assets, posx, posy, "caixa")
                        groups['all_blocks'].add(element)
                        groups['breakables'].add(element)
                        groups['all_sprites'].add(element)
                
                    elif value == "m":
                        element = Collectable(assets, posx, posy, "moeda", index=[i,j])
                        if element.index not in collected:
                            groups['collectibles'].add(element)
                            groups['all_sprites'].add(element)
                
                    elif value == "b":
                        element = Flag(assets, posx, posy, "bandeira animada")
                        groups['all_sprites'].add(element)

                        element = Collectable(assets, posx, posy, "bandeira", index=[i,j])
                        if element.index not in collected:
                            groups['collectibles'].add(element)
                            groups['all_sprites'].add(element)

                    elif value in ["green", "blue", "red"] and value not in current_colors:
                        element = Collectable(assets, posx, posy, f"prisma_{value}", prism=value, index=[i,j])
                        if element.index not in collected:
                            groups['collectibles'].add(element)
                            groups['all_sprites'].add(element)

    return groups

def colisao_minima(player, bloco):
    minimo = SIZE/4
    if player.rect.right > bloco.rect.left > player.rect.left:
        if (player.rect.right - bloco.rect.left) > minimo:
            return True
    elif player.rect.right > bloco.rect.right > player.rect.left:
        if (bloco.rect.right - player.rect.left) > minimo:
            return True
    elif player.rect.centerx > bloco.rect.left and player.rect.centerx < bloco.rect.right:
        return True
    return False


def draw_infos(window, assets, player):
    # Desenhando o score
    score = assets['score_font'].render(f"{player.points:08d}", True, COLORS['yellow'])
    score_rect = score.get_rect()
    score_rect.midtop = (WIDTH / 2,  10)

    # Desenhando as vidas
    lifes = assets['score_font'].render(chr(9829) * player.lifes, True, COLORS['red'])
    lifes_rect = lifes.get_rect()
    lifes_rect.bottomleft = (22, HEIGHT - 10)
    
    window.blit(score, score_rect) # score
    window.blit(lifes, lifes_rect) # vidas

    if 'green' in player.colors:
        border = 3
        now = pygame.time.get_ticks()
        elapsed_ticks = now - player.last_dash
        width = (elapsed_ticks)*(100/player.dash_delay) if elapsed_ticks < player.dash_delay else 100

        window.fill(COLORS['black'], (10, HEIGHT-SIZE, 100+2*border, 25)) # retângulo preto (borda)
        window.fill(COLORS['white'], (10+border, HEIGHT-SIZE+border, 100, 25-2*border)) # retângulo branco (fundo)
        window.fill(COLORS['yellow'], (10+border, HEIGHT-SIZE+border, width, 25-2*border)) # retangulo amarelo (energia do dash)
    
def save(DATA):
    data = json.dumps(DATA)
    with io.open('assets/save.json', "w", encoding='utf8"') as file:
        file.write(data)