from werkzeug.security import generate_password_hash  # vem junto com o Flask
from database import conectar  # reusamos a funcao do nosso database.py

def criar_administrador(usuario, senha):
    """Cria um administrador com a senha guardada de forma segura (hash)."""
    conexao = conectar()
    cursor = conexao.cursor()

    # Transforma a senha em um hash irreversivel ANTES de guardar
    senha_protegida = generate_password_hash(senha)

    # O '?' e' um espaco reservado: protege contra ataques de SQL Injection
    cursor.execute(
        "INSERT INTO usuarios (usuario, senha_hash) VALUES (?, ?)",
        (usuario, senha_protegida)
    )

    conexao.commit()
    conexao.close()
    print(f"Administrador '{usuario}' criado com sucesso!")

if __name__ == "__main__":
    # Troque por um usuario e senha de sua escolha
    criar_administrador("admin", "historia2025")