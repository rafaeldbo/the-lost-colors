from parameters import *
from sprites import *

def load_map(fase, assets):
    with open(f'assets/{fase}.csv', 'r') as arquivo:
        fase_lines = arquivo.readlines()
    matriz_fase = []
    for linha in fase_lines:
        linha = linha.strip()
        linha = linha.split(';')
        for i, block in enumerate(linha):
            linha[i] = block
        matriz_fase.append(linha)

    groups = {
        'all_enemys': pygame.sprite.Group(),
        'all_blocks': pygame.sprite.Group(),
        'all_fireballs': pygame.sprite.Group(),
        'collectibles': pygame.sprite.Group(),
        'all_sprites': pygame.sprite.Group(),
    }

    for i, linha in enumerate(matriz_fase):
        for j, block in enumerate(linha):
            if block != "0":
                posx = SIZE*j - SIZE*3
                posy = SIZE*i - SIZE*1
                if block == "c":
                    element = Block(assets, posx, posy, "chao")
                    groups['all_blocks'].add(element)
                elif block == "p":
                    element = Block(assets, posx, posy, "parede")
                    groups['all_blocks'].add(element)
                elif block == "i":
                    element = Enemy(assets, posx, posy, "inimigo chao")
                    groups['all_enemys'].add(element)
                elif block == "e":
                    element = Block(assets, posx, posy, "espinhos")
                    groups['all_enemys'].add(element)
                elif block == "d":
                    element = Collectable(assets, posx, posy, "diamante", diamond='red')
                    groups['collectibles'].add(element)
                elif block == "m":
                    element = Collectable(assets, posx, posy, "moeda")
                    groups['collectibles'].add(element)
                groups['all_sprites'].add(element)
    return groups

def colisao_minima(player, bloco):
    minimo = SIZE/6
    if player.rect.right > bloco.rect.left > player.rect.left:
        if (player.rect.right - bloco.rect.left) > minimo:
            return True
    elif player.rect.right > bloco.rect.right > player.rect.left:
        if (bloco.rect.right - player.rect.left) > minimo:
            return True
    elif player.rect.centerx > bloco.rect.left:
        return True
    return False