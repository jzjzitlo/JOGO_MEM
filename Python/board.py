# Importa as bibliotecas
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import random
from result import show_result

# Lista global que armazenará os IDs das cartas selecionadas para o jogo
cards = []
after_ids = []  # Lista para armazenar os IDs das callbacks do after, para cancelar depois

# Função que garante que um número (ID da carta) não se repita na lista de cartas
def verify_card(result):
    # Enquanto o número sorteado já estiver na lista, sorteia outro
    while result in cards:
        result = random.randint(1, 52)
    return result

# Cria uma lista com 24 cartas únicas (ID entre 1 e 52)
def create_deck_id():
    cards.clear()  # Lista para armazenar os IDs das cartas
    for _ in range(24):
        result = verify_card(random.randint(1, 52))
        cards.append(result)
    return cards

# Cria o baralho duplicando cada imagem (pares) e embaralha a lista
def create_deck_cards(cards):
    deck = []
    for card_id in cards:
        img = Image.open(f"imagens/cards/{card_id}.png")  # Abre a imagem da carta pelo ID
        img = ImageTk.PhotoImage(img)  # Converte para imagem compatível com Tkinter
        deck.append(img)  # Adiciona primeira cópia
        deck.append(img)  # Adiciona segunda cópia (par)
    random.shuffle(deck)  # Embaralha o baralho
    return deck

# Função principal que inicia o tabuleiro do jogo
def start_board(player1, player2):
    # Cria a janela principal
    window = ctk.CTk()
    window.geometry("1920x1080")  # Define tamanho da janela
    window.title("Memory Game")  # Título da janela
    window.resizable(True, True)  # Permite redimensionamento

    # Gera os IDs das cartas e cria o baralho com imagens
    card_ids = create_deck_id()
    deck = create_deck_cards(card_ids)

    # Cria o topo da interface com placar e informações
    frame_top = ctk.CTkFrame(window, height=80)
    frame_top.pack(fill="x")  # Ocupa largura total

    # Variáveis de controle de pontuação e turno
    current_turn = tk.StringVar(value=f"Vez: {player1}")  # Turno atual, inicializei com o jogador 1 para um bom fluxo de jogo
    score1 = tk.IntVar(value=0)  # Pontuação do jogador 1, uso o tk.IntVar para atualizar automaticamente e não precisar de .get()
    score2 = tk.IntVar(value=0)  # Pontuação do jogador 2
    player_turn = [1]  # Lista mutável para controlar de quem é a vez (1 ou 2)

    # Título do jogo
    label_title = ctk.CTkLabel(frame_top, text="Memory Game", font=("Arial", 24))
    label_title.pack(side="top", pady=5)

    # Frame com as informações dos jogadores e turno
    info_frame = ctk.CTkFrame(frame_top)
    info_frame.pack(fill="x", pady=5)

    # Rótulos com os nomes e pontuações
    player1_label = ctk.CTkLabel(info_frame, textvariable=tk.StringVar(value=f"{player1} - Pontos:"), font=("Arial", 18))
    player1_score = ctk.CTkLabel(info_frame, textvariable=score1, font=("Arial", 18))
    player2_label = ctk.CTkLabel(info_frame, textvariable=tk.StringVar(value=f"{player2} - Pontos:"), font=("Arial", 18))
    player2_score = ctk.CTkLabel(info_frame, textvariable=score2, font=("Arial", 18))
    turn_label = ctk.CTkLabel(info_frame, textvariable=current_turn, font=("Arial", 18))

    # Posicionamento dos elementos
    player1_label.pack(side="left", padx=10)
    player1_score.pack(side="left")
    player2_score.pack(side="right", padx=10)
    player2_label.pack(side="right")
    turn_label.pack(side="top", pady=5)

    # Cria um canvas com scroll para exibir as cartas
    scroll_canvas = tk.Canvas(window, bg="#363636", height=820)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    # Posiciona o canvas e a barra de rolagem
    scrollbar.pack(side="right", fill="y")
    scroll_canvas.pack(side="left", fill="both", expand=True)

    # Cria um frame interno para colocar os botões das cartas
    inner_frame = ctk.CTkFrame(scroll_canvas, fg_color="#363636")
    scroll_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Função chamada sempre que o tamanho do frame interno mudar, por exemplo, 
    # coloco uma carta, essa função é chamada para garantir o funcionamento do scrollbar, caso ele seja necessario
    def on_configure(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    # Associa evento de redimensionamento
    inner_frame.bind("<Configure>", on_configure)

    # Imagem da parte de trás das cartas (coberta)
    back_img = ImageTk.PhotoImage(Image.open("imagens/cards/back.png").resize((128, 128)))

    revealed = []# Lista para controlar quais cartas foram reveladas
    image_refs = []  # Referências para manter imagens em memória

    # Função que verifica se duas cartas abertas são um par
    checking = [False] #flag para gerenciar o numero de verificacoes, garantindo que apenas uma verificação ocorra por vez
    def check_match():
        checking [0] = False #define a flag como falsa, para evitar simultaneas verificacoes.

        def clear_after(): #utilizado para elimininar os callbacks que after executa, fazendo com que na reexecucao do programa, nenhum callback cause erros.
            for after_id in after_ids:
                scroll_canvas.after_cancel(after_id)
            after_ids.clear()

    
        if len(revealed) == 2: # A função só deve rodar se exatamente 2 cartas estiverem viradas
        
            idx1, id1 = revealed[0]# Pega os índices e IDs únicos das duas cartas reveladas, idx é o índice, e id1 é o id da carta. 
            idx2, id2 = revealed[1]#Todas as cartas possuem como nome seu id, indo de 1 a 52
            
            # Compara se as imagens nas duas posições do baralho são iguais
            if deck[idx1] == deck[idx2]:
                # Se for a vez do jogador 1, adiciona 1 ponto a ele
                if player_turn[0] == 1:
                    score1.set(score1.get() + 24)
                else:
                    # Se for a vez do jogador 2, adiciona 1 ponto a ele
                    score2.set(score2.get() + 1)
            else:
                # Se as cartas forem diferentes:
                # Aguarda 1 segundo e vira as cartas de volta (recoloca imagem de trás)
                after_ids.append(scroll_canvas.after(700, lambda: card_buttons[idx1].configure(image=back_img)))
                after_ids.append(scroll_canvas.after(700, lambda: card_buttons[idx2].configure(image=back_img)))
                
                # Alterna o jogador da vez
                player_turn[0] = 2 if player_turn[0] == 1 else 1
                current_turn.set(f"Vez: {player1 if player_turn[0] == 1 else player2}")
            
            # Limpa a lista de cartas reveladas, independente de acerto ou erro
            revealed.clear()

            # Verifica se todas as 24 combinações foram feitas (fim de jogo)
            if score1.get() + score2.get() == 24:
                # Determina o vencedor e perdedor, armazenando a pontuacao de cada um, que vai ser mandada para a funcao show_result()
                winner = player1 if score1.get() > score2.get() else player2
                loser = player2 if score1.get() > score2.get() else player1
                points = score1.get() if score1.get() > score2.get() else score2.get()
                loser_points = score2.get() if score1.get() > score2.get() else score1.get()
                # Cancela todas as chamadas pendentes do after
                clear_after()
                # Fecha a janela do jogo e mostra o resultado final
                window.destroy()
                show_result(winner, points, loser, loser_points)


    card_buttons = []  # Lista para armazenar os botões das cartas

    # Cria e posiciona os 48 botões (24 pares)
    for idx in range(48):
        row, col = divmod(idx, 8)  # Calcula linha e coluna para grade 8x6 por meio da função divmod
                                    #(descobri essa funcao pelo gpt, retorna tanto o valor inteiro da divisão 
                                    # quanto o resto. O valor inteiro representa a linha em que o elemento sera posicionado, 
                                    # e o resto a coluna.)
        card_button = tk.Label(inner_frame, image=back_img, bg="#363636")  # Cria carta coberta
        card_button.grid(row=row, column=col, padx=10, pady=10)  # Posiciona na grade
        image_refs.append(deck[idx])  # Guarda referência da imagem

        # Função que retorna a função de clique específica para cada botão
        def make_click(i):
            def click(event):
                # Se menos de 2 cartas estão reveladas e a carta clicada está coberta
                if len(revealed) < 2 and card_buttons[i]['image'] == str(back_img):
                    card_buttons[i].configure(image=deck[i])  # Revela a carta
                    revealed.append((i, id(card_buttons[i])))  # Salva info da carta revelada
                    if not checking[0]:  # Só agenda se nenhuma verificação estiver pendente
                        checking[0] = True
                        after_ids.append(scroll_canvas.after(700, check_match))# Chama verificação após 0.7s
                        
            return click

        card_button.bind("<Button-1>", make_click(idx))  # Associa clique à carta
        card_buttons.append(card_button)  # Armazena o botão

    # Inicia o loop da interface gráfica
    window.mainloop()
