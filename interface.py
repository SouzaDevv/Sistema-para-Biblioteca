import tkinter as tk
from tkinter import ttk, messagebox
from programa import (
    registrar_emprestimo,
    devolver_livro,
    editar_emprestimo,
    listar_emprestimos_ativos,
    listar_vencendo,
    buscar_emprestimos,
    registrar_livro,
    listar_acervo,
)


AMARELO = "#F5C400"
PRETO = "#1A1A1A"
BRANCO = "#FFFFFF"


def iniciar_app():
    janela = tk.Tk()
    janela.title("Sistema de Empréstimo de Livros")
    janela.geometry("850x520")
    janela.configure(bg=PRETO)


    estilo = ttk.Style()
    estilo.theme_use("clam")

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

<<<<<<< HEAD
=======

>>>>>>> a07d9a29f0f781f9493ffb69a6ed902ba447f804
    estilo.configure("TFrame", background=BRANCO)
    estilo.configure("TLabel", background=BRANCO, foreground=PRETO, font=("Segoe UI", 10))
    estilo.configure("Titulo.TLabel", background=BRANCO, foreground=PRETO, font=("Segoe UI", 13, "bold"))

    estilo.configure(
        "Amarelo.TButton",
        background=AMARELO,
        foreground=PRETO,
        font=("Segoe UI", 10, "bold"),
        padding=(10, 8),
        borderwidth=0,
    )
    estilo.map("Amarelo.TButton", background=[("active", "#D9AC00")])

<<<<<<< HEAD
=======

>>>>>>> a07d9a29f0f781f9493ffb69a6ed902ba447f804
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
    aba_acervo = ttk.Frame(abas, style="TFrame")
    aba_ativos = ttk.Frame(abas, style="TFrame")
    aba_atencao = ttk.Frame(abas, style="TFrame")

    abas.add(aba_cadastrar, text="Cadastrar Empréstimo")
    abas.add(aba_acervo, text="Acervo")
    abas.add(aba_ativos, text="Empréstimos Ativos")
    abas.add(aba_atencao, text="Atenção")


    combo_livro = None

    def carregar_titulos_acervo():
        return [livro["titulo"] for livro in listar_acervo()]


    ttk.Label(aba_cadastrar, text="Novo Empréstimo", style="Titulo.TLabel").grid(
        row=0, column=0, columnspan=2, padx=20, pady=(20, 15), sticky="w"
    )

    ttk.Label(aba_cadastrar, text="Nome do aluno:").grid(row=1, column=0, padx=20, pady=8, sticky="w")
    entrada_aluno = tk.Entry(aba_cadastrar, width=35, relief="solid", borderwidth=1)
    entrada_aluno.grid(row=1, column=1, padx=20, pady=8)

    ttk.Label(aba_cadastrar, text="Série/turma (ex: 1º B):").grid(row=2, column=0, padx=20, pady=8, sticky="w")
    entrada_serie = tk.Entry(aba_cadastrar, width=35, relief="solid", borderwidth=1)
    entrada_serie.grid(row=2, column=1, padx=20, pady=8)

    ttk.Label(aba_cadastrar, text="Livro:").grid(row=3, column=0, padx=20, pady=8, sticky="w")
    combo_livro = ttk.Combobox(aba_cadastrar, width=33, state="readonly")
    combo_livro.grid(row=3, column=1, padx=20, pady=8)

    ttk.Label(aba_cadastrar, text="Prazo (dias):").grid(row=4, column=0, padx=20, pady=8, sticky="w")
    entrada_prazo = tk.Entry(aba_cadastrar, width=35, relief="solid", borderwidth=1)
    entrada_prazo.grid(row=4, column=1, padx=20, pady=8)

    def ao_clicar_registrar():
        aluno = entrada_aluno.get().strip()
        serie = entrada_serie.get().strip()
        livro = combo_livro.get().strip()
        prazo_texto = entrada_prazo.get().strip()

        if not aluno or not serie or not livro or not prazo_texto:
            messagebox.showwarning("Campos vazios", "Preencha aluno, série, livro e prazo.")
            return

        try:
            dias_prazo = int(prazo_texto)
        except ValueError:
            messagebox.showwarning("Prazo inválido", "O prazo precisa ser um número de dias (ex: 7).")
            return

        try:
            data_devolucao = registrar_emprestimo(aluno, serie, livro, dias_prazo)
        except ValueError as erro:
            messagebox.showwarning("Sem exemplares", str(erro))
            return

        messagebox.showinfo("Sucesso", f"Empréstimo registrado!\nDevolver até: {data_devolucao}")

        entrada_aluno.delete(0, tk.END)
        entrada_serie.delete(0, tk.END)
        combo_livro.set("")
        entrada_prazo.delete(0, tk.END)

        atualizar_lista_ativos()
        atualizar_lista_atencao()
        atualizar_tabela_acervo()

    ttk.Button(
        aba_cadastrar, text="Registrar Empréstimo", style="Amarelo.TButton", command=ao_clicar_registrar
    ).grid(row=5, column=0, columnspan=2, pady=20)

<<<<<<< HEAD

    ttk.Label(aba_acervo, text="Cadastrar / Atualizar Livro", style="Titulo.TLabel").grid(
        row=0, column=0, columnspan=2, padx=20, pady=(20, 15), sticky="w"
=======

    colunas = ("id", "aluno", "livro", "data_emprestimo", "data_devolucao_prevista")

    ttk.Label(aba_ativos, text="Empréstimos Ativos", style="Titulo.TLabel").pack(
        anchor="w", padx=15, pady=(15, 10)
>>>>>>> a07d9a29f0f781f9493ffb69a6ed902ba447f804
    )

    ttk.Label(aba_acervo, text="Título do livro:").grid(row=1, column=0, padx=20, pady=8, sticky="w")
    entrada_titulo_livro = tk.Entry(aba_acervo, width=35, relief="solid", borderwidth=1)
    entrada_titulo_livro.grid(row=1, column=1, padx=20, pady=8)

    ttk.Label(aba_acervo, text="Quantidade de exemplares:").grid(row=2, column=0, padx=20, pady=8, sticky="w")
    entrada_quantidade = tk.Entry(aba_acervo, width=35, relief="solid", borderwidth=1)
    entrada_quantidade.grid(row=2, column=1, padx=20, pady=8)

    def ao_clicar_cadastrar_livro():
        titulo = entrada_titulo_livro.get().strip()
        quantidade_texto = entrada_quantidade.get().strip()

        if not titulo or not quantidade_texto:
            messagebox.showwarning("Campos vazios", "Preencha título e quantidade.")
            return

        try:
            quantidade = int(quantidade_texto)
        except ValueError:
            messagebox.showwarning("Quantidade inválida", "A quantidade precisa ser um número inteiro.")
            return

        registrar_livro(titulo, quantidade)
        messagebox.showinfo("Sucesso", f"'{titulo}' cadastrado com {quantidade} exemplar(es).")

        entrada_titulo_livro.delete(0, tk.END)
        entrada_quantidade.delete(0, tk.END)

        atualizar_tabela_acervo()

    ttk.Button(
        aba_acervo, text="Salvar Livro", style="Amarelo.TButton", command=ao_clicar_cadastrar_livro
    ).grid(row=3, column=0, columnspan=2, pady=15)

    colunas_acervo = ("titulo", "quantidade_total", "emprestados", "disponivel")
    titulos_acervo = ["Título", "Total", "Emprestados", "Disponíveis"]

    tabela_acervo = ttk.Treeview(aba_acervo, columns=colunas_acervo, show="headings", height=10)
    for coluna, titulo in zip(colunas_acervo, titulos_acervo):
        tabela_acervo.heading(coluna, text=titulo)
        tabela_acervo.column(coluna, width=140)
    tabela_acervo.grid(row=4, column=0, columnspan=2, padx=20, pady=15, sticky="nsew")

    def atualizar_tabela_acervo():
        for linha in tabela_acervo.get_children():
            tabela_acervo.delete(linha)

        for livro in listar_acervo():
            tabela_acervo.insert("", "end", values=(
                livro["titulo"],
                livro["quantidade_total"],
                livro["emprestados"],
                livro["disponivel"],
            ))


        combo_livro["values"] = carregar_titulos_acervo()


    colunas = ("id", "aluno", "serie", "livro", "data_emprestimo", "data_devolucao_prevista")
    titulos_colunas = ["ID", "Aluno", "Série", "Livro", "Emprestado em", "Devolver até"]

    ttk.Label(aba_ativos, text="Empréstimos Ativos", style="Titulo.TLabel").pack(
        anchor="w", padx=15, pady=(15, 5)
    )

    frame_busca = tk.Frame(aba_ativos, bg=BRANCO)
    frame_busca.pack(fill="x", padx=15, pady=5)

    ttk.Label(frame_busca, text="Buscar (aluno, série ou livro):").pack(side="left")
    entrada_busca = tk.Entry(frame_busca, width=30, relief="solid", borderwidth=1)
    entrada_busca.pack(side="left", padx=8)

    tabela_ativos = ttk.Treeview(aba_ativos, columns=colunas, show="headings", height=11)
    for coluna, titulo in zip(colunas, titulos_colunas):
        tabela_ativos.heading(coluna, text=titulo)
        tabela_ativos.column(coluna, width=110)
    tabela_ativos.pack(padx=15, pady=5, fill="both", expand=True)

    def preencher_tabela_ativos(lista_emprestimos):
        for linha in tabela_ativos.get_children():
            tabela_ativos.delete(linha)

        for emprestimo in lista_emprestimos:
            tabela_ativos.insert("", "end", values=(
                emprestimo["id"],
                emprestimo["aluno"],
                emprestimo["serie"],
                emprestimo["livro"],
                emprestimo["data_emprestimo"],
                emprestimo["data_devolucao_prevista"],
            ))

    def atualizar_lista_ativos():
        preencher_tabela_ativos(listar_emprestimos_ativos())

    def ao_clicar_buscar():
        termo = entrada_busca.get().strip()
        if termo:
            preencher_tabela_ativos(buscar_emprestimos(termo))
        else:
            atualizar_lista_ativos()

    def ao_limpar_busca():
        entrada_busca.delete(0, tk.END)
        atualizar_lista_ativos()

    ttk.Button(frame_busca, text="Buscar", style="Amarelo.TButton", command=ao_clicar_buscar).pack(
        side="left", padx=5
    )
    ttk.Button(frame_busca, text="Limpar", style="Amarelo.TButton", command=ao_limpar_busca).pack(
        side="left", padx=5
    )

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
        atualizar_tabela_acervo()

    def abrir_janela_editar():
        selecionado = tabela_ativos.selection()
        if not selecionado:
            messagebox.showwarning("Nada selecionado", "Clique num empréstimo da lista antes de editar.")
            return

        item = tabela_ativos.item(selecionado[0])
        id_emprestimo, aluno_atual, serie_atual, livro_atual, _, _ = item["values"]

        janela_editar = tk.Toplevel(janela)
        janela_editar.title("Editar Empréstimo")
        janela_editar.geometry("350x280")
        janela_editar.configure(bg=BRANCO)

        ttk.Label(janela_editar, text="Aluno:", background=BRANCO).pack(pady=(15, 0))
        campo_aluno = tk.Entry(janela_editar, width=30, relief="solid", borderwidth=1)
        campo_aluno.insert(0, aluno_atual)
        campo_aluno.pack(pady=5)

        ttk.Label(janela_editar, text="Série/turma:", background=BRANCO).pack()
        campo_serie = tk.Entry(janela_editar, width=30, relief="solid", borderwidth=1)
        campo_serie.insert(0, serie_atual)
        campo_serie.pack(pady=5)

        ttk.Label(janela_editar, text="Livro:", background=BRANCO).pack()
        campo_livro = ttk.Combobox(janela_editar, width=27, state="readonly")
        campo_livro["values"] = carregar_titulos_acervo()
        campo_livro.set(livro_atual)
        campo_livro.pack(pady=5)

        ttk.Label(janela_editar, text="Novo prazo (dias a partir de hoje):", background=BRANCO).pack()
        campo_prazo = tk.Entry(janela_editar, width=30, relief="solid", borderwidth=1)
        campo_prazo.insert(0, "7")
        campo_prazo.pack(pady=5)

        def salvar_edicao():
            novo_aluno = campo_aluno.get().strip()
            nova_serie = campo_serie.get().strip()
            novo_livro = campo_livro.get().strip()
            prazo_texto = campo_prazo.get().strip()

            if not novo_aluno or not nova_serie or not novo_livro or not prazo_texto:
                messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
                return

            try:
                dias = int(prazo_texto)
            except ValueError:
                messagebox.showwarning("Prazo inválido", "O prazo precisa ser um número de dias.")
                return

            editar_emprestimo(id_emprestimo, novo_aluno, nova_serie, novo_livro, dias)
            messagebox.showinfo("Sucesso", "Empréstimo atualizado!")

            janela_editar.destroy()
            atualizar_lista_ativos()
            atualizar_lista_atencao()
            atualizar_tabela_acervo()

        ttk.Button(
            janela_editar, text="Salvar alterações", style="Amarelo.TButton", command=salvar_edicao
        ).pack(pady=15)

    frame_botoes_ativos = tk.Frame(aba_ativos, bg=BRANCO)
    frame_botoes_ativos.pack(pady=10)

    ttk.Button(
        frame_botoes_ativos, text="Marcar como Devolvido", style="Amarelo.TButton", command=ao_clicar_devolver
    ).pack(side="left", padx=5)
    ttk.Button(
        frame_botoes_ativos, text="Editar Registro", style="Amarelo.TButton", command=abrir_janela_editar
    ).pack(side="left", padx=5)
    ttk.Button(
        frame_botoes_ativos, text="Atualizar Lista", style="Amarelo.TButton", command=atualizar_lista_ativos
    ).pack(side="left", padx=5)


    ttk.Label(aba_atencao, text="Prazos Vencendo", style="Titulo.TLabel").pack(
        anchor="w", padx=15, pady=(15, 10)
    )

    tabela_atencao = ttk.Treeview(aba_atencao, columns=colunas, show="headings", height=12)
    for coluna, titulo in zip(colunas, titulos_colunas):
        tabela_atencao.heading(coluna, text=titulo)
        tabela_atencao.column(coluna, width=110)
    tabela_atencao.pack(padx=15, pady=5, fill="both", expand=True)

    def atualizar_lista_atencao():
        for linha in tabela_atencao.get_children():
            tabela_atencao.delete(linha)

        itens_vencendo = listar_vencendo()

        for emprestimo in itens_vencendo:
            tabela_atencao.insert("", "end", values=(
                emprestimo["id"],
                emprestimo["aluno"],
                emprestimo["serie"],
                emprestimo["livro"],
                emprestimo["data_emprestimo"],
                emprestimo["data_devolucao_prevista"],
            ))

<<<<<<< HEAD
=======

>>>>>>> a07d9a29f0f781f9493ffb69a6ed902ba447f804
        quantidade = len(itens_vencendo)
        if quantidade > 0:
            abas.tab(aba_atencao, text=f"⚠️ Atenção ({quantidade})")
        else:
            abas.tab(aba_atencao, text="Atenção")

    ttk.Button(
        aba_atencao, text="Atualizar Lista", style="Amarelo.TButton", command=atualizar_lista_atencao
    ).pack(pady=10)

    # Carga inicial
    atualizar_tabela_acervo()
    atualizar_lista_ativos()
    atualizar_lista_atencao()

    janela.mainloop()


if __name__ == "__main__":
    iniciar_app()
