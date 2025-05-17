import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import random
from result import show_result

cards = []

def verify_card(result):
    while result in cards:
        result = random.randint(1, 52)
    return result

def create_deck_id():
    for _ in range(24):
        result = verify_card(random.randint(1, 52))
        cards.append(result)
    return cards

def create_deck_cards(cards):
    deck = []
    for card_id in cards:
        img = Image.open(f"imagens/cards/{card_id}.png")
        img = ImageTk.PhotoImage(img)
        deck.append(img)
        deck.append(img)
    random.shuffle(deck)
    return deck

def start_board(player1, player2):
    window = ctk.CTk()
    window.geometry("1920x1080")
    window.title("Memory Game")
    window.resizable(True, True)

    card_ids = create_deck_id()
    deck = create_deck_cards(card_ids)

    frame_top = ctk.CTkFrame(window, height=80)
    frame_top.pack(fill="x")

    current_turn = tk.StringVar(value=f"Vez: {player1}")
    score1 = tk.IntVar(value=0)
    score2 = tk.IntVar(value=0)
    player_turn = [1]

    label_title = ctk.CTkLabel(frame_top, text="Memory Game", font=("Arial", 24))
    label_title.pack(side="top", pady=5)

    info_frame = ctk.CTkFrame(frame_top)
    info_frame.pack(fill="x", pady=5)

    player1_label = ctk.CTkLabel(info_frame, textvariable=tk.StringVar(value=f"{player1} - Pontos:"), font=("Arial", 18))
    player1_score = ctk.CTkLabel(info_frame, textvariable=score1, font=("Arial", 18))
    player2_label = ctk.CTkLabel(info_frame, textvariable=tk.StringVar(value=f"{player2} - Pontos:"), font=("Arial", 18))
    player2_score = ctk.CTkLabel(info_frame, textvariable=score2, font=("Arial", 18))
    turn_label = ctk.CTkLabel(info_frame, textvariable=current_turn, font=("Arial", 18))

    player1_label.pack(side="left", padx=10)
    player1_score.pack(side="left")
    player2_score.pack(side="right", padx=10)
    player2_label.pack(side="right")
    turn_label.pack(side="top", pady=5)

    scroll_canvas = tk.Canvas(window, bg="#363636", height=820)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    scroll_canvas.pack(side="left", fill="both", expand=True)

    inner_frame = ctk.CTkFrame(scroll_canvas, fg_color="#363636")
    scroll_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def on_configure(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    inner_frame.bind("<Configure>", on_configure)

    back_img = ImageTk.PhotoImage(Image.open("imagens/cards/back.png").resize((128, 128)))

    revealed = []
    image_refs = []

    def check_match():
        if len(revealed) == 2:
            idx1, id1 = revealed[0]
            idx2, id2 = revealed[1]
            if deck[idx1] == deck[idx2]:
                if player_turn[0] == 1:
                    score1.set(score1.get() + 1)
                else:
                    score2.set(score2.get() + 1)
            else:
                scroll_canvas.after(1000, lambda: card_buttons[idx1].configure(image=back_img))
                scroll_canvas.after(1000, lambda: card_buttons[idx2].configure(image=back_img))
                player_turn[0] = 2 if player_turn[0] == 1 else 1
                current_turn.set(f"Vez: {player1 if player_turn[0] == 1 else player2}")
            revealed.clear()

            if score1.get() + score2.get() == 24:
                winner = player1 if score1.get() > score2.get() else player2
                loser = player2 if score1.get() > score2.get() else player1
                points = score1.get() if score1.get() > score2.get() else score2.get()
                loser_points = score2.get() if score1.get() > score2.get() else score1.get()
                window.after(600,show_result(winner, points, loser, loser_points))

    card_buttons = []

    for idx in range(48):
        row, col = divmod(idx, 8)
        card_button = tk.Label(inner_frame, image=back_img, bg="#363636")
        card_button.grid(row=row, column=col, padx=10, pady=10)
        image_refs.append(deck[idx])

        def make_click(i):
            def click(event):
                if len(revealed) < 2 and card_buttons[i]['image'] == str(back_img):
                    card_buttons[i].configure(image=deck[i])
                    revealed.append((i, id(card_buttons[i])))
                    scroll_canvas.after(500, check_match)
            return click

        card_button.bind("<Button-1>", make_click(idx))
        card_buttons.append(card_button)

    window.mainloop()
