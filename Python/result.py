import customtkinter as ctk

def show_result(winner, points, loser, loser_points):
    window = ctk.CTk()
    window.geometry("600x400")
    window.resizable(True, True)
    window.title("Resultado Final")

    label = ctk.CTkLabel(window, text="Fim de Jogo!", font=("Arial", 32))
    label.pack(pady=20)

    winner_label = ctk.CTkLabel(window, text=f"Vencedor: {winner}", font=("Arial", 24))
    winner_label.pack(pady=10)

    points_label = ctk.CTkLabel(window, text=f"Pontos: {points}", font=("Arial", 24))
    points_label.pack(pady=10)

    loser_label = ctk.CTkLabel(window, text=f"Perdedor: {loser}", font=("Arial", 24))
    loser_label.pack(pady=10)

    loser_points_label = ctk.CTkLabel(window, text=f"Pontos: {loser_points}", font=("Arial", 24))
    loser_points_label.pack(pady=10)

    button = ctk.CTkButton(window, text="Sair", command=window.destroy)
    button.pack(pady=30)

    window.mainloop()
