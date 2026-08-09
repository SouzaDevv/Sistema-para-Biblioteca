# 📚 Sistema de Empréstimo de Livros

Sistema desktop desenvolvido para digitalizar o controle de empréstimos de livros de uma biblioteca escolar, substituindo o antigo controle manual em planilhas Excel.

## Sobre o projeto

O sistema permite que o responsável pela biblioteca registre empréstimos, controle devoluções e acompanhe prazos de vencimento de forma simples e organizada, tudo em uma interface visual local, sem necessidade de internet ou instalação de dependências externas.

## Funcionalidades

- **Cadastro de empréstimos** — registra aluno, livro e prazo de devolução
- **Lista de empréstimos ativos** — visualização de tudo que está emprestado no momento
- **Aba de atenção** — destaca automaticamente os empréstimos próximos do vencimento ou já vencidos
- **Registro de devolução** — marca empréstimos como devolvidos sem perder o histórico

## Tecnologias utilizadas

- **Python** — linguagem principal do projeto
- **Tkinter** — interface gráfica desktop
- **SQLite** — banco de dados local, sem necessidade de servidor
- **PyInstaller** — empacotamento do sistema em executável (.exe) standalone

## Arquitetura

O projeto foi estruturado seguindo separação de responsabilidades:

```
main.py        → ponto de entrada do programa
interface.py   → camada visual (Tkinter)
logica.py      → regras de negócio
banco.py       → acesso e persistência de dados (SQLite)
```

Essa divisão isola a lógica de negócio da interface e do banco de dados, facilitando manutenção e futuras expansões.

## Como executar

```bash
python -m venv venv
venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
python main.py
```

## Autor

Desenvolvido por Giovanni, estudante de Ciência de Dados na FATEC Votorantim.