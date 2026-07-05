from flask import Flask, session
from database import conectar

from routes.auth_routes import auth
from routes.produto_routes import produto
from routes.moto_routes import moto
from routes.ordem_routes import ordem
from routes.usuario_routes import usuario

import sqlite3
import os

app = Flask(__name__)
app.secret_key = "segredo123"

# =========================
# UPLOAD DE IMAGENS
# =========================
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB

# =========================
# BANCO
# =========================

conn = conectar()
cursor = conn.cursor()

# =========================
# USUÁRIOS
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    senha TEXT,
    tipo TEXT,
    nome TEXT,
    telefone TEXT,
    email TEXT
)
""")

# =========================
# PRODUTOS
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    quantidade INTEGER,
    preco REAL
)
""")

# =========================
# MOTOS
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS motos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    modelo TEXT,
    marca TEXT,
    placa TEXT,
    ano TEXT,
    problema TEXT,
    foto TEXT
)
""")

# Atualiza bancos antigos
colunas = [
    ("problema", "TEXT"),
    ("foto", "TEXT")
]

for coluna, tipo in colunas:
    try:
        cursor.execute(f"ALTER TABLE motos ADD COLUMN {coluna} {tipo}")
    except sqlite3.OperationalError:
        pass

# =========================
# ORDENS
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ordens(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    cliente TEXT,
    moto TEXT,
    servico TEXT,
    valor REAL,
    status TEXT
)
""")

# =========================
# NOTIFICAÇÕES
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS notificacoes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    mensagem TEXT,
    lida INTEGER DEFAULT 0,
    data TEXT
)
""")

conn.commit()

# =========================
# CRIAR ADMIN
# =========================

admin = cursor.execute(
    "SELECT * FROM usuarios WHERE usuario=?",
    ("admin",)
).fetchone()

if not admin:
    cursor.execute("""
    INSERT INTO usuarios(
        usuario,
        senha,
        tipo,
        nome,
        telefone,
        email
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "admin",
        "123",
        "admin",
        "Administrador",
        "000000000",
        "admin@gmail.com"
    ))

    conn.commit()

conn.close()

# =========================
# BLUEPRINTS
# =========================

app.register_blueprint(auth)
app.register_blueprint(produto)
app.register_blueprint(moto)
app.register_blueprint(ordem)
app.register_blueprint(usuario)

from repositories.notificacao_repository import contar_nao_lidas

# =========================
# MENU
# =========================

@app.context_processor
def notificacoes_menu():

    if "usuario" in session:
        return {
            "total_notificacoes": contar_nao_lidas(session["usuario"])
        }

    return {
        "total_notificacoes": 0
    }

# =========================
# INICIAR
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )