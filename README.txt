README

1. Sobre o projeto
Este é um jogo da memória feito em Python com uma interface gráfica moderna usando a biblioteca CustomTkinter. O jogo foi pensado para dois jogadores e tem como objetivo encontrar pares de cartas iguais. Ele conta com uma tela inicial para entrada dos nomes, um sistema de pontuação automática e cartas embaralhadas aleatoriamente a cada partida.

2. Requisitos para instalação
Para rodar o projeto corretamente, você precisa ter o Python instalado em sua máquina. Além disso, é necessário instalar duas bibliotecas adicionais:

CustomTkinter

Pillow (PIL)

Você pode instalar essas bibliotecas usando o seguinte comando no terminal ou prompt de comando:

pip install customtkinter pillow

3. Estrutura do projeto
O projeto está dividido da seguinte forma:

imagens/: cards/: contém as imagens das cartas do baralho (nomes devem ser números de 1 a 52 no formato .png).

	Icon/: contém uma imagem chamada icon.png usada como logotipo na tela inicial.

cards.py: responsável por criar os IDs das cartas e gerar o baralho embaralhado com imagens.

menu_inicial.py: tela de entrada onde os jogadores informam seus nomes.

jogo_memoria.py: tela principal onde o jogo é exibido e acontece a lógica de virar cartas e pontuação.


4. Como executar o projeto

Verifique se o Python e as bibliotecas mencionadas estão instaladas.

Garanta que a pasta "imagens" esteja configurada com as imagens corretas:

52 imagens de cartas dentro de "imagens/cards", nomeadas como 1.png, 2.png, até 52.png.

Um ícone em "imagens/Icon/icon.png".

Execute o arquivo menu_inicial.py.

Após inserir os nomes dos dois jogadores e clicar em “Jogar”, a tela fecha. Você pode programar para que o jogo_memoria.py seja executado em seguida automaticamente, se quiser. Atualmente, isso precisa ser feito manualmente.


5. Funcionalidades principais

Interface gráfica moderna e responsiva com CustomTkinter

Dois jogadores com nomes personalizados

Sistema automático de pontuação

Cartas embaralhadas a cada rodada

Suporte à rolagem vertical para visualizar todas as cartas no tabuleiro

Uso de imagens reais de cartas de baralho

