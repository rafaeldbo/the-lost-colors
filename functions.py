from config import *
from sprites import *

def load_map(fase, assets, checkpoint, current_colors):
    with open(f'assets/{fase}.csv', 'r') as arquivo:
        fase_lines = arquivo.readlines()
    separator = fase_lines[1][1]
    matriz_fase = []
    colunas = {}
    for linha in fase_lines:
        linha = linha.strip()
        linha = linha.split(separator)
        for i, value in enumerate(linha):
            if i not in colunas.keys():
                colunas[i] = [value]
            elif i in colunas.keys():
                colunas[i].append(value)

    for j in range(checkpoint['inicio'], checkpoint['fim']):
        coluna = colunas[j]
        matriz_fase.append(coluna)

    groups = {
        'all_blocks': pygame.sprite.Group(), # Todos os blocos que possuem colisão
        'all_enemys': pygame.sprite.Group(), # Todas as entidades que causam dano
        'all_fireballs': pygame.sprite.Group(), # Bolas de fogo (destruem entidades)
        'collectibles': pygame.sprite.Group(), # Todas as entidades Coletaveis
        'flag': pygame.sprite.Group(), # Bandeira
        'breakables': pygame.sprite.Group(), # Todas as entidades quebraveis com Bola de Fogo
        'all_sprites': pygame.sprite.Group(), # Todas as Entidades
    }

    for j, coluna in enumerate(matriz_fase):
        for i, value in enumerate(coluna):
            if value != "0":
                posx = SIZE*j - checkpoint['parede']
                posy = SIZE*i

                if value == "c":
                    element = Block(assets, posx, posy, "chao")
                    groups['all_blocks'].add(element)

                elif value == "p":
                    element = Block(assets, posx, posy, "parede")
                    groups['all_blocks'].add(element)

                elif value == "i1":
                    element = Enemy(assets, posx, posy, "inimigo chao","horizontal")
                    groups['all_enemys'].add(element)
                    groups['breakables'].add(element)

                elif value == "i2":
                    element = Enemy(assets, posx, posy, "inimigo chao","vertical")
                    groups['all_enemys'].add(element)
                    groups['breakables'].add(element)

                elif value == "e":
                    element = Block(assets, posx, posy, "espinhos")
                    groups['all_enemys'].add(element)
                
                elif value == "q":
                    element = Block(assets, posx, posy, "caixa")
                    groups['all_blocks'].add(element)
                    groups['breakables'].add(element)
                
                elif value == "m":
                    element = Collectable(assets, posx, posy, "moeda")
                    groups['collectibles'].add(element)
                
                elif value == "b":
                    element = Flag(assets, posx, posy, "bandeira")
                    groups['flag'].add(element)

                elif value in ["green", "blue", "red"] and value not in current_colors:
                    element = Collectable(assets, posx, posy, f"prisma_{value}", prism=value)
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
    elif player.rect.centerx > bloco.rect.left:
        return True
    return False