from parameters import *
from sprites import *

def load_map(fase, assets):
    with open(f'assets/{fase}.csv', 'r') as arquivo:
        fase_lines = arquivo.readlines()
    separator = fase_lines[1][1]
    matriz_fase = []
    for linha in fase_lines:
        linha = linha.strip()
<<<<<<< HEAD
        linha = linha.split(separator)
=======
        linha = linha.split(';')
        linha = "".join(linha).split(',')
>>>>>>> 889af025794a99fa4cc281d253f26dbdcd6c3ea5
        for i, block in enumerate(linha):
            linha[i] = block
        matriz_fase.append(linha)

    groups = {
<<<<<<< HEAD
        'all_blocks': pygame.sprite.Group(), # Todos os blocos que possuem colisão
        'all_enemys': pygame.sprite.Group(), # Todas as entidades que causam dano
        'all_fireballs': pygame.sprite.Group(), # Bolas de fogo (destruem entidades)
        'collectibles': pygame.sprite.Group(), # Todas as entidades Coletaveis
        'breakables': pygame.sprite.Group(), # Todas as entidades quebraveis com Bola de Fogo
        'all_sprites': pygame.sprite.Group(), # Todas as Entidades
=======
        'all_enemys': pygame.sprite.Group(),
        'all_blocks': pygame.sprite.Group(),
        'all_fireballs': pygame.sprite.Group(),
        'collectibles': pygame.sprite.Group(),
        'all_sprites': pygame.sprite.Group(),
        'all_smashblocks': pygame.sprite.Group()
>>>>>>> 889af025794a99fa4cc281d253f26dbdcd6c3ea5
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
                    groups['breakables'].add(element)

                elif block == "e":
                    element = Block(assets, posx, posy, "espinhos")
                    groups['all_enemys'].add(element)
                
                elif block == "q":
                    element = Block(assets, posx, posy, "caixa")
                    groups['all_blocks'].add(element)
                    groups['breakables'].add(element)
                
                elif block == "m":
                    element = Collectable(assets, posx, posy, "moeda")
                    groups['collectibles'].add(element)
<<<<<<< HEAD

                elif block in ["green", "blue", "red"]:
                    element = Collectable(assets, posx, posy, f"prisma_{block}", prism=block)
                    groups['collectibles'].add(element)

=======
                elif block == "s":
                    element = SmashBlock (assets, posx, posy, "smash_blocks")
                    groups["all_smashblocks"].add(element)
>>>>>>> 889af025794a99fa4cc281d253f26dbdcd6c3ea5
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