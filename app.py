from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

print(__name__)

@app.route("/pague")
def exiba_mensagem():
    return "<h2>Pagar as pessoas, faz bem as pessoas!!!</h2>"

@app.route("/")
def mensagem_home():
    return "<h1>Bem-vindo a API dos Livros</h1>"

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute(""" 
            CREATE TABLE IF NOT EXISTS LIVROS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                image_url TEXT NOT NULL
            )
    """)

init_db()

@app.route("/doar", methods=["POST"])
def doar():

    dados = request.get_json()

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")

    if not titulo or not categoria or not autor or not image_url:
        return jsonify({"erro" : "todos os campos são obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:
        conn.execute(f"""
        INSERT INTO LIVROS (titulo, categoria, autor, image_url)
        VALUES ("{titulo}", "{categoria}", "{autor}", "{image_url}")
""")

    conn.commit()

    return jsonify({"mensagem": "Livro Cadastrado com sucesso"}), 201

@app.route("/livros", methods=["GET"])
def listar_livros():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LIVROS")
        livros = cursor.fetchall()
        return jsonify(livros), 200

if __name__ == "__main__":
    app.run(debug=True)
