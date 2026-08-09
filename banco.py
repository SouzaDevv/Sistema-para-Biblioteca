import sqlite3


def criar_tabela():
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT NOT NULL,
            serie TEXT NOT NULL,
            livro TEXT NOT NULL,
            data_emprestimo TEXT NOT NULL,
            data_devolucao_prevista TEXT NOT NULL,
            data_devolucao_real TEXT,
            status TEXT NOT NULL
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL UNIQUE,
            quantidade INTEGER NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def listar_emprestimos_ativos(filtro=None):
    conexao = sqlite3.connect("biblioteca.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    if filtro:
        termo = f"%{filtro}%"
        cursor.execute("""
            SELECT id, aluno, serie, livro, data_emprestimo, data_devolucao_prevista, status
            FROM emprestimos
            WHERE status = 'Emprestado'
            AND (aluno LIKE ? OR serie LIKE ? OR livro LIKE ?)
        """, (termo, termo, termo))
    else:
        cursor.execute("""
            SELECT id, aluno, serie, livro, data_emprestimo, data_devolucao_prevista, status
            FROM emprestimos
            WHERE status = 'Emprestado'
        """)

    linhas = cursor.fetchall()
    conexao.close()

    return linhas


def salvar_emprestimo(aluno, serie, livro, data_emprestimo, data_devolucao_prevista, status):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO emprestimos (aluno, serie, livro, data_emprestimo, data_devolucao_prevista, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (aluno, serie, livro, str(data_emprestimo), str(data_devolucao_prevista), status))

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


def atualizar_emprestimo(id_emprestimo, aluno, serie, livro, data_devolucao_prevista):
    """Edita os dados de um empréstimo já existente (correção de erro de digitação, etc)."""
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE emprestimos
        SET aluno = ?, serie = ?, livro = ?, data_devolucao_prevista = ?
        WHERE id = ?
    """, (aluno, serie, livro, str(data_devolucao_prevista), id_emprestimo))

    conexao.commit()
    conexao.close()


def contar_emprestados(titulo_livro):
    """Quantos exemplares desse título estão emprestados agora."""
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM emprestimos
        WHERE livro = ? AND status = 'Emprestado'
    """, (titulo_livro,))

    quantidade = cursor.fetchone()[0]
    conexao.close()

    return quantidade




def cadastrar_livro(titulo, quantidade):
    conexao = sqlite3.connect("biblioteca.db")
    cursor = conexao.cursor()


    cursor.execute("""
        INSERT INTO livros (titulo, quantidade)
        VALUES (?, ?)
        ON CONFLICT(titulo) DO UPDATE SET quantidade = excluded.quantidade
    """, (titulo, quantidade))

    conexao.commit()
    conexao.close()


def listar_livros():
    conexao = sqlite3.connect("biblioteca.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    cursor.execute("SELECT id, titulo, quantidade FROM livros ORDER BY titulo")
    linhas = cursor.fetchall()
    conexao.close()

    return linhas


if __name__ == "__main__":
    criar_tabela()