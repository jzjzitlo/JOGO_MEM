# === IMPORTANDO AS FERRAMENTAS ===

import tkinter as tk  # Biblioteca para criar janelas e botões
import customtkinter as ctk  # Versão estilizada do tkinter
from PIL import Image, ImageTk  # Usada para abrir e mostrar imagens
from cards import create_deck_id as create_cards  # Cria os IDs das cartas
from cards import create_deck_cards as create_deck  # Cria as imagens embaralhadas das cartas


# === CONFIGURAÇÃO DA JANELA PRINCIPAL ===

window = ctk.CTk()  # Criamos a janela
window.geometry("1600x900")  # Tamanho da janela
window.title("Memory Game")  # Título da janela
window.resizable(False, False)  # Não deixa redimensionar
ctk.set_appearance_mode("dark")  # Modo escuro


# === CRIANDO O BARALHO ===

card = create_cards()  # Gera os pares
cards = create_deck(card)  # Embaralha e pega as imagens


# === CRIANDO O CANVAS (ÁREA DO JOGO) ===

canvas = ctk.CTkCanvas(window, width=1600, height=900)  # Área onde as cartas vão aparecer
canvas.configure(bg="#363636")  # Cor de fundo
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)  # Scroll
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)


# === IMAGEM DAS CARTAS VIRADAS (COSTAS) ===

img_path = "imagens/cards/back.png"
img_pil = Image.open(img_path)  # Abre a imagem
img = ImageTk.PhotoImage(img_pil)  # Prepara para ser usada no canvas


# === FUNÇÕES DO JOGO ===

# Volta a carta para a imagem virada para baixo
def hide_card(image_id):
    canvas.itemconfig(image_id, image=img)

# Quando o jogador clica em uma carta
def on_click(event, row, col):
    print(f"Imagem clicada: linha={row}, coluna={col}")  # Apenas mostra onde clicou para controle de desenvolvimento
    image_id = image_ids[(row, col)]  # Pega a imagem clicada
    index = row * 8 + col  # Calcula o índice da carta (0 a 47)
    canvas.itemconfig(image_id, image=cards[index])  # Mostra a carta verdadeira
    canvas.after(2000, lambda: hide_card(image_id))  # Espera 2 segundos e vira novamente


# === TAMANHO DAS CARTAS ===

card_width = 128
card_height = 128
padding = 10


# === VARIÁVEIS DE JOGO ===

image_ids = {}  # Guardará os IDs das imagens
player1points = 0
player2points = 0

# === TÍTULOS E PONTUAÇÃO ===
# aqui, labels são criadas para mostrar o título do jogo e os pontos dos jogadores
label = ctk.CTkLabel(canvas, text="Memory Game", font=("Arial", 24), text_color="white")
label.place(x=700, y=10)

player1_label = ctk.CTkLabel(canvas, text=f"Player 1 \n pontos:{player1points}", font=("Arial", 18), text_color="white")
player1_label.place(x=100, y=10)

player2_label = ctk.CTkLabel(canvas, text=f"Player 2 \n pontos:{player2points}", font=("Arial", 18), text_color="white")
player2_label.place(x=1400, y=10)


# === DESENHANDO AS 48 CARTAS ===

for idx in range(48):
    row = idx // 8  # Linha (0 a 5)
    col = idx % 8   # Coluna (0 a 7)
    x = 210 + col * (card_width + padding)  # Posição X
    y = 50 + row * (card_height + padding)  # Posição Y

    tag = f"card_{row}_{col}"  # Nome da carta
    image_id = canvas.create_image(x, y, image=img, anchor="nw", tags=(tag))  # Coloca a carta virada
    image_ids[(row, col)] = image_id  # Salva o ID dessa carta
    # Diz o que acontece quando clicamos nela, chamando a função on_click
    canvas.tag_bind(tag, "<Button-1>", lambda event, row=row, col=col: on_click(event, row, col))


# Atualiza a rolagem se o tamanho da tela mudar
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Faz o canvas rolar quando a tela mudar(caso o canvas atualize, o
# bind ativa e executa a função on_configure, caso o tamanho do canvas ultrapasse o da tela)
canvas.bind("<Configure>", on_configure)

# === INICIA O JOGO ===
window.mainloop()
