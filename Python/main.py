# Importa bibliotecas necessárias
import random as rd                   
import customtkinter as ctk          
from tkinter import ttk              
import time as tm                    
from PIL import Image, ImageTk       
import os                            

# Função que pega os nomes digitados pelos jogadores
def get_names():
    name1 = str(entry1.get())        # Lê o texto digitado no campo do jogador 1
    name2 = str(entry2.get())        # Lê o texto digitado no campo do jogador 2
    window.after(600, window.destroy) # Espera 600 milissegundos e fecha a janela
    print(name1, name2)              # Mostra os nomes no terminal (teste)
    return name1, name2              # Retorna os nomes (caso queira usar em outro lugar)

# Cria a janela principal
window = ctk.CTk()
window.geometry("1600x900")          # Define tamanho da janela
window.title("Memory Game")          # Título da janela
window.resizable(False, False)       # Não permite redimensionar a janela

# Organiza o espaço da janela com linhas e colunas usando grid
for i in range(8):                   # Cria 8 linhas
    for j in range(3):               # Cria 3 colunas
        window.grid_rowconfigure(i, weight=1)
        window.grid_columnconfigure(j, weight=1)

# Ajusta tamanhos mínimos e pesos de algumas linhas
window.grid_rowconfigure(6, minsize=60, weight=0)
window.grid_rowconfigure(7, minsize=50, weight=0)
window.grid_rowconfigure(3, minsize=0, weight=0)
window.grid_rowconfigure(5, minsize=0, weight=0)
window.grid_rowconfigure(1, minsize=0, weight=0)
window.grid_rowconfigure(2, minsize=100, weight=0)

# Cria o fundo da tela (canvas é como um quadro onde se desenha)
canvas = ctk.CTkCanvas(window, width=1920, height=1080)
canvas.grid(row=0, column=0, columnspan=3, rowspan=8, padx=0, pady=0)

# Caminho da imagem do ícone (ajuste o caminho se mover o arquivo)
img_path = "imagens/Icon/icon.png"

# Abre a imagem
img = Image.open(img_path)

# Redimensiona a imagem para 100x100
img = img.resize((100, 100))

# Converte a imagem para usar no tkinter
img = ImageTk.PhotoImage(img)

# Define cor de fundo do canvas e adiciona textos e imagem central
canvas.configure(bg="#363636")
canvas.create_text(800, 100, text="Memory Game", font=("Arial", 40), fill="white")
canvas.create_image(800, 200, anchor='center', image=img)
canvas.create_text(800, 300, text="Insira o nome do jogador 1", font=("Arial", 25), fill="white")
canvas.create_text(800, 500, text="Insira o nome do jogador 2", font=("Arial", 25), fill="white")

# Cria campos para digitar o nome dos jogadores
entry1 = ctk.CTkEntry(window, placeholder_text="Nome do jogador 1", width=200, height=50, font=("Arial", 20))
entry2 = ctk.CTkEntry(window, placeholder_text="Nome do jogador 2", width=200, height=50, font=("Arial", 20))

# Coloca os campos na tela (em posições do canvas)
canvas.create_window(800, 400, window=entry1, width=300, height=50)
canvas.create_window(800, 600, window=entry2, width=300, height=50)

# Cria o botão "Jogar" que chama a função get_names quando clicado
button = ctk.CTkButton(window, text="Jogar", font=("Arial", 20), command=lambda: [get_names()], width=200, height=50)

# Cria o botão "Sair" para fechar o programa
button_exit = ctk.CTkButton(window, text="Sair", font=("Arial", 20), fg_color="red", command=window.destroy, width=200, height=50, hover_color="darkred")

# Adiciona os botões no canvas
canvas.create_window(800, 700, window=button)
canvas.create_window(800, 800, window=button_exit)

# Inicia a janela
window.mainloop()
