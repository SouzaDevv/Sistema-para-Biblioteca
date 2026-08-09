from datetime import date, timedelta, datetime
from banco import salvar_emprestimo, atualizar_status_emprestimo, listar_emprestimos_ativos


def registrar_emprestimo(aluno, serie, livro, dias_prazo):
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