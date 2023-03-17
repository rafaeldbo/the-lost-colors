import json, io
from config import *
from sprites import *

# Carrega a matriz da fase
def load_matriz(fase):
    # Lê o arquivo da matriz
    with open(f'assets/{fase}.csv', 'r') as arquivo:
        fase_lines = arquivo.readlines()
    separator = fase_lines[1][1]

    # Cria uma nova matriz transformando as colunas em linhas e linhas em colunas
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

    # Retorna a matriz gerada
    return matriz_fase


"""
    Explicação dos checkpoints:

    Os checkpoints foram criados para deixar o jogo mais 'leve'.
    
    Como o player não varia sua posição em x mas sim os objetos, era preciso
    muito processamento para mover todos os objetos da fase.
        
    A fase foi dividida em trechos mais curtos, cada checkpoint tem um valor
    da coluna onde o trecho que vai ser carregado inicia 
    e um valor da coluna onde o trecho termina. 
    Assim o trecho anterior deixa de existir e apenas os objetos do novo trecho
    precisam ser movidos.       
    
"""
# Carrega o trecho da matriz referente ao último checkpoint
def load_map(assets, fase, player):
    matriz_fase = load_matriz(fase)
    checkpoint = GAME[fase]['checkpoints'][player.checkpoint]
    collected = player.collected
    current_colors = player.colors
    # Cria os grupos
    groups = {
        'blocks': pygame.sprite.Group(), # Todos os Blocos {possuem colisão}
        'enemys': pygame.sprite.Group(), # Todas os Monstros (possuem movimento)
        'fireballs': pygame.sprite.Group(), # Tadas as Bolas de fogo (destruem entidades)
        'collectibles': pygame.sprite.Group(), # Todas as Entidades Coletaveis
        'breakables': pygame.sprite.Group(), # Todas as Entidades Quebraveis com Bola de Fogo
        'damagers': pygame.sprite.Group(), # Todas as Entidade que causam Dano
        'all_sprites': pygame.sprite.Group(), # Todas as Entidades
    }

    # Lê a matriz gerada pela load_matriz
    for j, coluna in enumerate(matriz_fase):
        # Gera apenas o trecho referente ao último checkpoint
        if j in range(checkpoint['inicio'], checkpoint['fim']):
            for i, value in enumerate(coluna):
                # Identifica qual é o elemento 
                # Cria o objeto e adiciona ele ao referente grupo
                
                if value != "0":
                    posx = SIZE*j - checkpoint['parede'] - checkpoint['inicio']*SIZE
                    posy = SIZE*i

                    if value == "c":
                        element = Block(assets, posx, posy, "chao")
                        groups['blocks'].add(element)
                        groups['all_sprites'].add(element)

                    elif value == "p":
                        element = Block(assets, posx, posy, "parede")
                        groups['blocks'].add(element)
                        groups['all_sprites'].add(element)

                    elif value == "i1":
                        element = Enemy(assets, posx, posy, "inimigo", "horizontal")
                        groups['enemys'].add(element)
                        groups['damagers'].add(element)
                        groups['breakables'].add(element)
                        groups['all_sprites'].add(element)

                    elif value == "i2":
                        element = Enemy(assets, posx, posy, "inimigo", "vertical")
                        groups['enemys'].add(element)
                        groups['damagers'].add(element)
                        groups['breakables'].add(element)
                        groups['all_sprites'].add(element)

                    elif value == "e":
                        element = Block(assets, posx, posy, "espinhos")
                        groups['damagers'].add(element)
                        groups['all_sprites'].add(element)
                
                    elif value == "q":
                        element = Block(assets, posx, posy, "caixa")
                        groups['blocks'].add(element)
                        groups['breakables'].add(element)
                        groups['all_sprites'].add(element)
                
                    elif value == "m":
                        element = Coin(assets, posx, posy, "moeda", index=[i,j])
                        if element.index not in collected:
                            groups['collectibles'].add(element)
                            groups['all_sprites'].add(element)
                
                    elif value == "b":
                        element = Flag(assets, posx, posy, "bandeira", index=[i,j])
                        groups['all_sprites'].add(element)

                        if element.index not in collected:
                            groups['collectibles'].add(element)
                            groups['all_sprites'].add(element)

                    elif value in ["green", "blue", "red"] and value not in current_colors:
                        element = Prism(assets, posx, posy, f"prisma_{value}", value, index=[i,j])
                        if element.index not in collected:
                            groups['collectibles'].add(element)
                            groups['all_sprites'].add(element)

    return groups

# Verifica se a colisão é 'válida', evita que o player escale a parede
def colisao_minima(player, bloco):
    minimo = SIZE/4
    # Parte da frente do rect do player está em cima do bloco
    if player.rect.right > bloco.rect.left > player.rect.left:
        if (player.rect.right - bloco.rect.left) > minimo:
            return True
    # Parte de trás do rect do player está em cima do bloco
    elif player.rect.right > bloco.rect.right > player.rect.left:
        if (bloco.rect.right - player.rect.left) > minimo:
            return True
    # O centro do rect do player está em cima do bloco
    elif player.rect.centerx > bloco.rect.left and player.rect.centerx < bloco.rect.right:
        return True
    return False

# desenha as informações de vidas, score e barra do dash
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

    # Se o player já tem o diamante verde, desenha a barra do dash
    # A barra do dash indica se já se passou o tempo necessário
    # para o player utilizar o dash novamente
    if 'green' in player.colors:
        border = 3
        now = pygame.time.get_ticks()
        elapsed_ticks = now - player.last_dash
        # O tamanho da barra amarela é proporcional ao tempo decorrido
        # entre o momento atual e o último dash
        width = (elapsed_ticks)*(100/DASH_DELAY) if elapsed_ticks < DASH_DELAY else 100

        window.fill(COLORS['black'], (10, HEIGHT-SIZE, 100+2*border, 25)) # retângulo preto (borda)
        window.fill(COLORS['white'], (10+border, HEIGHT-SIZE+border, 100, 25-2*border)) # retângulo branco (fundo)
        window.fill(COLORS['yellow'], (10+border, HEIGHT-SIZE+border, width, 25-2*border)) # retangulo amarelo (energia do dash)

# função para salvar os dados do player (pontuações e cores coletadas)
def save(DATA):
    data = json.dumps(DATA)
    with io.open('assets/save.json', "w", encoding='utf8"') as file:
        file.write(data)