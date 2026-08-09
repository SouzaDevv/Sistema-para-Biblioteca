import sqlite3


def criar_tabela():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT NOT NULL,
            livro TEXT NOT NULL,
            data_emprestimo TEXT NOT NULL,
            data_devolucao_prevista TEXT NOT NULL,
            data_devolucao_real TEXT,
            status TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def listar_emprestimos_ativos():
    conexao = sqlite3.connect("biblioteca.db")
    conexao.row_factory = sqlite3.Row 
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, aluno, livro, data_emprestimo, data_devolucao_prevista, status
        FROM emprestimos
        WHERE status = 'Emprestado'
    """)

    linhas = cursor.fetchall()
    conexao.close()

    return linhas


def salvar_emprestimo(aluno, livro, data_emprestimo, data_devolucao_prevista, status):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO emprestimos (aluno, livro, data_emprestimo, data_devolucao_prevista, status)
        VALUES (?, ?, ?, ?, ?)
    """, (aluno, livro, str(data_emprestimo), str(data_devolucao_prevista), status))

    conexao.commit()
    conexao.close()


def atualizar_status_emprestimo(id_emprestimo, novo_status, data_devolucao_real):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE emprestimos
        SET status = ?, data_devolucao_real = ?
        WHERE id = ?
    """, (novo_status, str(data_devolucao_real), id_emprestimo))

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criar_tabela()
