from datetime import date, timedelta, datetime
from banco import (
    salvar_emprestimo,
    atualizar_status_emprestimo,
    atualizar_emprestimo,
    listar_emprestimos_ativos,
    contar_emprestados,
    cadastrar_livro,
    listar_livros,
)


def registrar_emprestimo(aluno, serie, livro, dias_prazo):
    disponivel = verificar_disponibilidade(livro)
    if disponivel is not None and disponivel <= 0:
        raise ValueError(f"Não há exemplares disponíveis de '{livro}' no momento.")

    hoje = date.today()
    data_devolucao = hoje + timedelta(days=dias_prazo)

    salvar_emprestimo(
        aluno=aluno,
        serie=serie,
        livro=livro,
        data_emprestimo=hoje,
        data_devolucao_prevista=data_devolucao,
        status="Emprestado"
    )

    return data_devolucao


def devolver_livro(id_emprestimo):
    data_devolucao_real = date.today()

    atualizar_status_emprestimo(
        id_emprestimo=id_emprestimo,
        novo_status="devolvido",
        data_devolucao_real=data_devolucao_real
    )


def editar_emprestimo(id_emprestimo, aluno, serie, livro, dias_prazo):
    """Corrige os dados de um empréstimo já registrado."""
    hoje = date.today()
    nova_data_devolucao = hoje + timedelta(days=dias_prazo)

    atualizar_emprestimo(
        id_emprestimo=id_emprestimo,
        aluno=aluno,
        serie=serie,
        livro=livro,
        data_devolucao_prevista=nova_data_devolucao,
    )

    return nova_data_devolucao


def listar_vencendo(dias_alerta=3):
    ativos = listar_emprestimos_ativos()
    hoje = date.today()

    vencendo = []
    for emprestimo in ativos:
        data_prevista = datetime.strptime(emprestimo["data_devolucao_prevista"], "%Y-%m-%d").date()
        dias_restantes = (data_prevista - hoje).days
        if dias_restantes <= dias_alerta:
            vencendo.append(emprestimo)

    return vencendo


def buscar_emprestimos(filtro):
    """Busca empréstimos ativos filtrando por aluno, série ou livro."""
    return listar_emprestimos_ativos(filtro=filtro)




def registrar_livro(titulo, quantidade):
    cadastrar_livro(titulo, quantidade)


def listar_acervo():
    """Retorna cada livro do acervo com a quantidade disponível calculada."""
    livros = listar_livros()
    resultado = []

    for livro in livros:
        emprestados = contar_emprestados(livro["titulo"])
        disponivel = livro["quantidade"] - emprestados
        resultado.append({
            "titulo": livro["titulo"],
            "quantidade_total": livro["quantidade"],
            "emprestados": emprestados,
            "disponivel": disponivel,
        })

    return resultado


def verificar_disponibilidade(titulo_livro):
    """Retorna quantos exemplares estão disponíveis, ou None se o livro não está cadastrado no acervo."""
    for livro in listar_acervo():
        if livro["titulo"] == titulo_livro:
            return livro["disponivel"]
    return None  