from banco import criar_tabela
from interface import iniciar_app

if __name__ == "__main__":
    criar_tabela()   # garante que a tabela existe antes de abrir a tela
    iniciar_app()
