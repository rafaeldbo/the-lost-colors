from parameters import *
from sprites import *

def load_map(fase, assets, groups):
    with open(f'assets/img/{fase}.csv', 'r') as arquivo:
        fase_lines = arquivo.readlines()
    matriz_fase = []
    for linha in fase_lines:
        linha = linha.strip()
        linha = linha.split(';')
        for i, block in enumerate(linha):
            linha[i] = block
        matriz_fase.append(linha)

    for i, linha in enumerate(matriz_fase):
        for j, block in enumerate(linha):
            if block != "0":
                posx = SIZE*j - SIZE*3
                posy = SIZE*i - SIZE*1
                if block == "c":
                    bloco = Block(assets['chao'], posx, posy)
                    groups['all_blocks'].add(bloco)
                elif block == "p":
                    bloco = Block(assets['parede'], posx, posy)  
                    groups['all_blocks'].add(bloco)
                elif block == "i":
                    monstro = Enemy(assets['monstro'], posx, posy)
                    groups['all_enemys'].add(monstro)
                elif block == "e":
                    espinhos = Block(assets['espinhos'], posx, posy + SIZE/2)
                    groups['all_enemys'].add(espinhos)
                elif block == "d":
                    diamante = Diamonds(assets['diamante'], posx, posy)
                    groups['diamond'].add(diamante)
                elif block == "m":
                    coin = Coin(assets['coin'], posx, posy)
                    groups['coins'].add(coin)
    return groups

def colisao_minima(player, bloco):
    minimo = SIZE/8
    if player.rect.right > bloco.rect.left > player.rect.left:
        if (player.rect.right - bloco.rect.left) > minimo:
            return True
    elif player.rect.right > bloco.rect.right > player.rect.left:
        if (bloco.rect.right - player.rect.left) > minimo:
            return True
    elif player.rect.centerx > bloco.rect.left:
        return True
    return False