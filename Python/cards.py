# Importa funções para gerar números aleatórios e para manipular imagens
from random import randint
import random
from PIL import Image, ImageTk

# Lista global para guardar os IDs únicos das cartas (números de 1 a 52)
cards = []

# Função que verifica se o número da carta já foi escolhido
def verify_card(result):
    # Se a carta já estiver na lista, sorteia outra até encontrar uma nova
    if result in cards:
        while result in cards:
            result = random.randint(1, 52)
    return result

# Cria um baralho com 24 cartas únicas (na verdade 12 pares de cartas)
def create_deck_id():
    for i in range(1, 25):
        # Sorteia um número de carta
        result = random.randint(1, 52)
        # Verifica se ela já foi sorteada e, se sim, muda
        result = verify_card(result)
        # Adiciona à lista final de cartas únicas
        cards.append(result)
    return cards

# Cria um baralho embaralhado com imagens das cartas (em pares)
def create_deck_cards(cards):
    deck = []
    
    for i in range(1, 25):
        # Abre a imagem correspondente ao ID da carta
        img = Image.open(f"imagens/cards/{cards[i-1]}.png")
        # Converte a imagem para o formato compatível com Tkinter
        img = ImageTk.PhotoImage(img)
        # Adiciona duas vezes a imagem no baralho (fazendo o par)
        deck.append(img)
        deck.append(img)
    
    # Embaralha todas as cartas do baralho
    random.shuffle(deck)
    return deck
