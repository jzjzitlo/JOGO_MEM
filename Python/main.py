import customtkinter as ctk
from PIL import Image, ImageTk
from board import start_board

def get_names():
    name1 = entry1.get()
    name2 = entry2.get()
    if name1 and name2:
        window.destroy()
        start_board(name1, name2)

window = ctk.CTk()
window.geometry("1920x1080")
window.title("Memory Game")
window.resizable(True, True)

canvas = ctk.CTkCanvas(window, width=1600, height=900)
canvas.pack(fill="both", expand=True)

img_path = "imagens/Icon/icon.png"
img = Image.open(img_path).resize((100, 100))
img = ImageTk.PhotoImage(img)

canvas.configure(bg="#363636")
canvas.create_text(960, 100, text="Memory Game", font=("Arial", 40), fill="white")
canvas.create_image(960, 200, anchor='center', image=img)
canvas.create_text(960, 300, text="Insira o nome do jogador 1", font=("Arial", 25), fill="white")
canvas.create_text(960, 500, text="Insira o nome do jogador 2", font=("Arial", 25), fill="white")

entry1 = ctk.CTkEntry(window, placeholder_text="Nome do jogador 1", width=300, height=50, font=("Arial", 20))
entry2 = ctk.CTkEntry(window, placeholder_text="Nome do jogador 2", width=300, height=50, font=("Arial", 20))

canvas.create_window(960, 400, window=entry1)
canvas.create_window(960, 600, window=entry2)

button = ctk.CTkButton(window, text="Jogar", command=get_names, font=("Arial", 20), width=200, height=50)
button_exit = ctk.CTkButton(window, text="Sair", command=window.destroy, font=("Arial", 20), fg_color="red", hover_color="darkred")

canvas.create_window(960, 700, window=button)
canvas.create_window(960, 900, window=button_exit)

window.mainloop()
