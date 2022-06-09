# The Lost Colors

## Contexto: 

Em The Lost Colors, um cientista roubou e aprisionou as cores do mundo em prismas, você deve pegar os 3 prismas referentes as cores primárias da luz (RGB), cada cor dará ao player um novo poder. Os poderes são: dash (prisma verde), pulo-duplo (prisma azul) e habilidade de atirar bolas de fogo (prisma vermelho). Os prismas funcionam como check-points, assim como as bandeiras inseridas no meio da fase, quando o player perde uma vida ele retorna para o último check-point coletado. Para vencer a fase você deve chegar a última bandeira. 

## Vídeo de Desmonstração:
- https://youtu.be/YhKGRmhBoVc

## Execuntando o Projeto:
- Para abrir o jogo execute o arquivo **game.py**

## Observação:

Para fins de facilitar o acesso e correção das duas fases do jogo, as cores requeridas para entrar na fase do laborátorio foram adicionadas ao **save.json**. Sem elas, só seria possível entrar nessa fase após completar a primeira. Caso precise, esvazie a lista **"cores"** do arquivo **save.json**.

## Créditos: 

### --> Criação da história do jogo: 
    Rafael Dourado Bastos de Oliveira

### --> Desenvolvimento do jogo:
    Alex Souza Pacchioni
    Beatriz Rodrigues de Freitas
    Rafael Dourado Bastos de Oliveira

### --> Criação da imagem do player:
    Mikael Henrique Preto

## Resumo do código: 

- **game.py**: Looping principal do jogo.
- A pasta assets contém outras pastas nas quais estão armazenados a fonte, as imagens e os sons utilizados. As imagens foram separadas por cor, já que alguns objetos mudam de cor quando um prisma é coletado, e também de acordo com as animações, cada animação possui uma pasta com suas imagens. 
- **init.py**: Menu inicial do jogo. 
- **end.py**: Menu final do jogo.
- **pause.py**: Menu de pause do jogo.
- **fase.py**: Código que executa as fases do jogo.
- **assets.py**: código responsável por carregar os arquivos do jogo (imagens, sons e fontes).
- **functions.py**: Funções globais do jogo.
- **config.py**: Váriaveis e dados globais do jogo.

## Referências:

- som da moeda ao ser coletada: https://www.youtube.com/watch?v=cTWE42VwZO0
- musica da fase floresta: https://www.youtube.com/watch?v=MMOtyRoNkUI
- musica da fase lab: https://www.youtube.com/watch?v=s_VcF1iEw90
- musica da tela inicial: https://www.youtube.com/watch?v=6TEGPexTqr4&t=1451s
- som da explosão: https://www.youtube.com/watch?v=dyPIyjtB3eM
- som do dash: https://www.youtube.com/watch?v=HDRVzwNkV20
- som do pulo: https://www.youtube.com/watch?v=561qHylVC_o
