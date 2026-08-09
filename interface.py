import tkinter as tk
from tkinter import ttk, messagebox
from programa import registrar_emprestimo, devolver_livro, listar_emprestimos_ativos, listar_vencendo

# ---------- Cores da escola ----------
AMARELO = "#F5C400"
PRETO = "#1A1A1A"
BRANCO = "#FFFFFF"


def iniciar_app():
    janela = tk.Tk()
    janela.title("Sistema de Empréstimo de Livros")
    janela.geometry("750x480")
    janela.configure(bg=PRETO)

    # ---------- Estilo geral ----------
    estilo = ttk.Style()
    estilo.theme_use("clam")

    # Abas
    estilo.configure("TNotebook", background=PRETO, borderwidth=0)
    estilo.configure(
        "TNotebook.Tab",
        background=PRETO,
        foreground=BRANCO,
        padding=(16, 8),
        font=("Segoe UI", 10, "bold"),
    )
    estilo.map(
        "TNotebook.Tab",
        background=[("selected", AMARELO)],
        foreground=[("selected", PRETO)],
    )

    # Frames internos
    estilo.configure("TFrame", background=BRANCO)

    # Labels
    estilo.configure("TLabel", background=BRANCO, foreground=PRETO, font=("Segoe UI", 10))
    estilo.configure("Titulo.TLabel", background=BRANCO, foreground=PRETO, font=("Segoe UI", 13, "bold"))

    # Botões
    estilo.configure(
        "Amarelo.TButton",
        background=AMARELO,
        foreground=PRETO,
        font=("Segoe UI", 10, "bold"),
        padding=(10, 8),
        borderwidth=0,
    )
    estilo.map("Amarelo.TButton", background=[("active", "#D9AC00")])

    # Tabela (Treeview)
    estilo.configure(
        "Treeview",
        background=BRANCO,
        fieldbackground=BRANCO,
        foreground=PRETO,
        rowheight=26,
        font=("Segoe UI", 9),
    )
    estilo.configure(
        "Treeview.Heading",
        background=PRETO,
        foreground=AMARELO,
        font=("Segoe UI", 9, "bold"),
    )
    estilo.map("Treeview", background=[("selected", AMARELO)], foreground=[("selected", PRETO)])

    abas = ttk.Notebook(janela)
    abas.pack(fill="both", expand=True, padx=8, pady=8)

    aba_cadastrar = ttk.Frame(abas, style="TFrame")
    aba_ativos = ttk.Frame(abas, style="TFrame")
    aba_atencao = ttk.Frame(abas, style="TFrame")

    abas.add(aba_cadastrar, text="Cadastrar")
    abas.add(aba_ativos, text="Empréstimos Ativos")
    abas.add(aba_atencao, text="Atenção")

    # ---------- ABA CADASTRAR ----------
    ttk.Label(aba_cadastrar, text="Novo Empréstimo", style="Titulo.TLabel").grid(
        row=0, column=0, columnspan=2, padx=20, pady=(20, 15), sticky="w"
    )

    ttk.Label(aba_cadastrar, text="Nome do aluno:").grid(row=1, column=0, padx=20, pady=8, sticky="w")
    entrada_aluno = tk.Entry(aba_cadastrar, width=35, relief="solid", borderwidth=1)
    entrada_aluno.grid(row=1, column=1, padx=20, pady=8)

    ttk.Label(aba_cadastrar, text="Livro:").grid(row=2, column=0, padx=20, pady=8, sticky="w")
    entrada_livro = tk.Entry(aba_cadastrar, width=35, relief="solid", borderwidth=1)
    entrada_livro.grid(row=2, column=1, padx=20, pady=8)

    ttk.Label(aba_cadastrar, text="Prazo (dias):").grid(row=3, column=0, padx=20, pady=8, sticky="w")
    entrada_prazo = tk.Entry(aba_cadastrar, width=35, relief="solid", borderwidth=1)
    entrada_prazo.grid(row=3, column=1, padx=20, pady=8)

    def ao_clicar_registrar():
        aluno = entrada_aluno.get().strip()
        livro = entrada_livro.get().strip()
        prazo_texto = entrada_prazo.get().strip()

        if not aluno or not livro or not prazo_texto:
            messagebox.showwarning("Campos vazios", "Preencha aluno, livro e prazo.")
            return

        try:
            dias_prazo = int(prazo_texto)
        except ValueError:
            messagebox.showwarning("Prazo inválido", "O prazo precisa ser um número de dias (ex: 7).")
            return

        data_devolucao = registrar_emprestimo(aluno, livro, dias_prazo)
        messagebox.showinfo("Sucesso", f"Empréstimo registrado!\nDevolver até: {data_devolucao}")

        entrada_aluno.delete(0, tk.END)
        entrada_livro.delete(0, tk.END)
        entrada_prazo.delete(0, tk.END)

        atualizar_lista_ativos()
        atualizar_lista_atencao()

    ttk.Button(
        aba_cadastrar, text="Registrar Empréstimo", style="Amarelo.TButton", command=ao_clicar_registrar
    ).grid(row=4, column=0, columnspan=2, pady=20)

    # ---------- ABA EMPRÉSTIMOS ATIVOS ----------
    colunas = ("id", "aluno", "livro", "data_emprestimo", "data_devolucao_prevista")

    ttk.Label(aba_ativos, text="Empréstimos Ativos", style="Titulo.TLabel").pack(
        anchor="w", padx=15, pady=(15, 10)
    )

    tabela_ativos = ttk.Treeview(aba_ativos, columns=colunas, show="headings", height=12)
    for coluna, titulo in zip(colunas, ["ID", "Aluno", "Livro", "Emprestado em", "Devolver até"]):
        tabela_ativos.heading(coluna, text=titulo)
        tabela_ativos.column(coluna, width=120)
    tabela_ativos.pack(padx=15, pady=5, fill="both", expand=True)

    def atualizar_lista_ativos():
        for linha in tabela_ativos.get_children():
            tabela_ativos.delete(linha)

        for emprestimo in listar_emprestimos_ativos():
            tabela_ativos.insert("", "end", values=(
                emprestimo["id"],
                emprestimo["aluno"],
                emprestimo["livro"],
                emprestimo["data_emprestimo"],
                emprestimo["data_devolucao_prevista"],
            ))

    def ao_clicar_devolver():
        selecionado = tabela_ativos.selection()
        if not selecionado:
            messagebox.showwarning("Nada selecionado", "Clique num empréstimo da lista antes de devolver.")
            return

        item = tabela_ativos.item(selecionado[0])
        id_emprestimo = item["values"][0]

        devolver_livro(id_emprestimo)
        messagebox.showinfo("Sucesso", "Livro marcado como devolvido!")

        atualizar_lista_ativos()
        atualizar_lista_atencao()

    frame_botoes_ativos = tk.Frame(aba_ativos, bg=BRANCO)
    frame_botoes_ativos.pack(pady=10)

    ttk.Button(
        frame_botoes_ativos, text="Marcar como Devolvido", style="Amarelo.TButton", command=ao_clicar_devolver
    ).pack(side="left", padx=5)
    ttk.Button(
        frame_botoes_ativos, text="Atualizar Lista", style="Amarelo.TButton", command=atualizar_lista_ativos
    ).pack(side="left", padx=5)

    # ---------- ABA ATENÇÃO ----------
    ttk.Label(aba_atencao, text="Prazos Vencendo", style="Titulo.TLabel").pack(
        anchor="w", padx=15, pady=(15, 10)
    )

    tabela_atencao = ttk.Treeview(aba_atencao, columns=colunas, show="headings", height=12)
    for coluna, titulo in zip(colunas, ["ID", "Aluno", "Livro", "Emprestado em", "Devolver até"]):
        tabela_atencao.heading(coluna, text=titulo)
        tabela_atencao.column(coluna, width=120)
    tabela_atencao.pack(padx=15, pady=5, fill="both", expand=True)

    def atualizar_lista_atencao():
        for linha in tabela_atencao.get_children():
            tabela_atencao.delete(linha)

        for emprestimo in listar_vencendo():
            tabela_atencao.insert("", "end", values=(
                emprestimo["id"],
                emprestimo["aluno"],
                emprestimo["livro"],
                emprestimo["data_emprestimo"],
                emprestimo["data_devolucao_prevista"],
            ))

    ttk.Button(
        aba_atencao, text="Atualizar Lista", style="Amarelo.TButton", command=atualizar_lista_atencao
    ).pack(pady=10)

    atualizar_lista_ativos()
    atualizar_lista_atencao()

    janela.mainloop()


if __name__ == "__main__":
    iniciar_app()