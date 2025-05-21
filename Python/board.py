import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import random
from result import show_result
from result import show_draw

# Classe que representa uma carta no tabuleiro
class MemoryCard:
    def __init__(self, master, front_img, back_img, card_id, click_callback, idx):
        self.front_img = front_img
        self.back_img = back_img
        self.card_id = card_id
        self.revealed = False
        self.idx = idx

        self.label = tk.Label(master, image=back_img, bg="#363636")
        self.label.image = back_img  # referência fixa
        self.label.bind("<Button-1>", lambda e: click_callback(self))

    def show(self):
        self.label.configure(image=self.front_img)
        self.label.image = self.front_img  # fixa frente

    def hide(self):
        self.label.configure(image=self.back_img)
        self.label.image = self.back_img  # fixa verso

    def grid(self, row, col):
        self.label.grid(row=row, column=col, padx=10, pady=10)

def create_deck():
    card_ids = random.sample(range(1, 53), 24)
    deck = []

    for cid in card_ids:
        path = f"imagens/Cards/{cid}.png"
        img1 = Image.open(path).resize((128, 128))
        photo1 = ImageTk.PhotoImage(img1)
        photo2 = ImageTk.PhotoImage(img1.copy())  # cópia evita conflito interno

        deck.append((photo1, cid))
        deck.append((photo2, cid))

    random.shuffle(deck)
    return deck

def create_board(player1, player2):
    window = ctk.CTk()
    window.geometry("1920x1080")
    window.title("Memory Game")
    window.resizable(True, True)

    # Variáveis de estado
    after_ids = []
    current_turn = tk.StringVar(value=f"Vez: {player1}")
    score1 = tk.IntVar(value=0)
    score2 = tk.IntVar(value=0)
    player_turn = [1]
    revealed_cards = []

    # Cabeçalho
    frame_top = ctk.CTkFrame(window, height=100)
    frame_top.pack(fill="x")
    ctk.CTkLabel(frame_top, text="Memory Game", font=("Arial", 28)).pack(pady=10)

    frame_info = ctk.CTkFrame(window, height=80)
    frame_info.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(frame_info, text=f"{player1} - Pontos:", font=("Arial", 23)).pack(side="left", padx=10)
    ctk.CTkLabel(frame_info, textvariable=score1, font=("Arial", 23)).pack(side="left")
    ctk.CTkLabel(frame_info, textvariable=current_turn, font=("Arial", 23)).pack(side="left", expand=True)
    ctk.CTkLabel(frame_info, textvariable=score2, font=("Arial", 23)).pack(side="right", padx=10)
    ctk.CTkLabel(frame_info, text=f"{player2} - Pontos:", font=("Arial", 23)).pack(side="right")

    # Tabuleiro
    frame_main = ctk.CTkFrame(window, fg_color="#363636")
    frame_main.pack(fill="both", expand=True)

    frame_grid = tk.Frame(frame_main, bg="#363636")
    frame_grid.place(relx=0.5, rely=0.5, anchor="center")

    # Imagem do verso da carta
    back_img = ImageTk.PhotoImage(Image.open("imagens/Cards/back.png").resize((128, 128)))

    # Cria as cartas
    deck_data = create_deck()
    cards = []

    def clear_after():
        for aid in after_ids:
            window.after_cancel(aid)
        after_ids.clear()

    def check_match():
        if len(revealed_cards) == 2:
            c1, c2 = revealed_cards
            if c1.card_id == c2.card_id:
                if player_turn[0] == 1:
                    score1.set(score1.get() + 1)
                else:
                    score2.set(score2.get() + 1)
            else:
                after_ids.append(window.after(1000, lambda: hide_cards(c1, c2)))
                player_turn[0] = 2 if player_turn[0] == 1 else 1
                current_turn.set(f"Vez: {player1 if player_turn[0] == 1 else player2}")
            revealed_cards.clear()

            if score1.get() + score2.get() == 24:
                clear_after()
                if score1.get() == score2.get():
                    window.destroy()
                    swow_draw(player1, player2)
                else:
                    winner = player1 if score1.get() > score2.get() else player2
                    loser = player2 if winner == player1 else player1
                    window.destroy()
                    show_result(winner, max(score1.get(), score2.get()), loser, min(score1.get(), score2.get()))

    def hide_cards(c1, c2):
        c1.hide()
        c1.revealed = False
        c2.hide()
        c2.revealed = False

    def on_card_click(card):
        if len(revealed_cards) < 2 and not card.revealed:
            card.show()
            card.revealed = True
            revealed_cards.append(card)
            if len(revealed_cards) == 2:
                check_match()

    # Monta as cartas no grid
    for i in range(48):
        img, cid = deck_data[i]
        card = MemoryCard(frame_grid, img, back_img, cid, on_card_click, i)
        card.grid(row=i // 8, col=i % 8)
        cards.append(card)

    window.mainloop()

# Execução
if __name__ == "__main__":
    create_board("Jogador 1", "Jogador 2")
