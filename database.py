import sqlite3  # modulo de banco SQLite, ja' embutido no Python

# Nome do arquivo onde o banco inteiro ficara' guardado
NOME_BANCO = "banco.db"

def conectar():
    """Abre (ou cria, se nao existir) o arquivo do banco e retorna a conexao."""
    conexao = sqlite3.connect(NOME_BANCO)
    # Faz cada linha vir como um dicionario {coluna: valor}, mais facil de usar
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabelas():
    """Cria as tabelas usuarios e eventos, se ainda nao existirem."""
    conexao = conectar()
    cursor = conexao.cursor()  # o cursor executa os comandos SQL

    # Tabela de administradores (atende H1 - login)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario     TEXT UNIQUE NOT NULL,
            senha_hash  TEXT NOT NULL
        )
    """)

    # Tabela de eventos do cronograma (atende H2, H3, H4, H5)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo       TEXT NOT NULL,
            palestrante  TEXT NOT NULL,
            local        TEXT,              -- preenchido se presencial
            link         TEXT,              -- preenchido se remoto
            data_hora    TEXT NOT NULL      -- formato ISO: AAAA-MM-DD HH:MM
        )
    """)

    conexao.commit()  # confirma (salva) as mudancas no arquivo
    conexao.close()   # fecha a conexao
    print("Tabelas criadas com sucesso!")

# Se rodarmos este arquivo diretamente, cria as tabelas
if __name__ == "__main__":
    criar_tabelas()


    