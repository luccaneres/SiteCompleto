from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import check_password_hash
from database import conectar, criar_tabelas

# Cria a aplicacao Flask. static_folder aponta para a pasta do frontend
app = Flask(__name__, static_folder="frontend", static_url_path="")

# Chave secreta: usada para assinar os cookies de login (sessao).
# Em producao, use um valor longo e aleatorio guardado em segredo.
app.secret_key = "troque-isto-por-algo-secreto-e-aleatorio"

# Garante que as tabelas existam quando o servidor iniciar
criar_tabelas()

# ---------- Rota para servir a pagina publica (frontend) ----------
@app.route("/")
def pagina_inicial():
    # Entrega o arquivo index.html da pasta frontend ao navegador
    return send_from_directory("frontend", "index.html")


@app.route("/api/login", methods=["POST"])
def login():
    # Le os dados JSON enviados pelo formulario do frontend
    dados = request.get_json()
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    # Busca o usuario no banco (note o ? contra SQL Injection)
    conexao = conectar()
    linha = conexao.execute(
        "SELECT * FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()  # fetchone = pega so' o primeiro resultado
    conexao.close()

    # Confere se existe E se a senha bate com o hash guardado
    if linha and check_password_hash(linha["senha_hash"], senha):
        session["logado"] = True          # marca a sessao como autenticada
        session["usuario"] = usuario
        return jsonify({"ok": True})      # responde sucesso em JSON
    else:
        # 401 = "nao autorizado" (codigo HTTP padrao para login invalido)
        return jsonify({"ok": False, "erro": "Credenciais invalidas"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()  # apaga os dados da sessao: usuario sai
    return jsonify({"ok": True})


@app.route("/api/eventos", methods=["GET"])
def listar_eventos():
    conexao = conectar()

    # AQUI esta' a magia da H4: ORDER BY data_hora ASC ja' devolve
    # os eventos do mais cedo ao mais tarde, automaticamente.
    linhas = conexao.execute(
        "SELECT * FROM eventos ORDER BY data_hora ASC"
    ).fetchall()  # fetchall = pega TODOS os resultados
    conexao.close()

    # Converte cada linha do banco em um dicionario (vira JSON depois)
    eventos = []
    for linha in linhas:
        eventos.append({
            "id": linha["id"],
            "titulo": linha["titulo"],
            "palestrante": linha["palestrante"],
            "local": linha["local"],
            "link": linha["link"],
            "data_hora": linha["data_hora"],
        })

    # jsonify transforma a lista Python em uma resposta JSON
    return jsonify(eventos)


def exige_login():
    """Retorna True se NAO estiver logado (para barrar a acao)."""
    return not session.get("logado")

@app.route("/api/eventos", methods=["POST"])  # H2: cadastrar
def criar_evento():
    if exige_login():
        return jsonify({"erro": "Faca login primeiro"}), 401

    d = request.get_json()  # dados do formulario de cadastro
    conexao = conectar()
    conexao.execute(
        """INSERT INTO eventos (titulo, palestrante, local, link, data_hora)
           VALUES (?, ?, ?, ?, ?)""",
        (d["titulo"], d["palestrante"], d.get("local"),
         d.get("link"), d["data_hora"])
    )
    conexao.commit()
    conexao.close()
    return jsonify({"ok": True}), 201  # 201 = "criado com sucesso"

@app.route("/api/eventos/<int:evento_id>", methods=["DELETE"])  # H3: remover
def remover_evento(evento_id):
    if exige_login():
        return jsonify({"erro": "Faca login primeiro"}), 401

    conexao = conectar()
    conexao.execute("DELETE FROM eventos WHERE id = ?", (evento_id,))
    conexao.commit()
    conexao.close()
    return jsonify({"ok": True})

# Liga o servidor em modo de desenvolvimento (com recarregamento automatico)
if __name__ == "__main__":
    app.run(debug=True, port=5000)