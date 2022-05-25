with open('assets/img/fase1.csv', 'r') as arquivo:
    fase = arquivo.readlines()
fase1 = []
for linha in fase:
    linha = linha.strip()
    linha = linha.split(';')
    for i, block in enumerate(linha):
        linha[i] = block
    fase1.append(linha)