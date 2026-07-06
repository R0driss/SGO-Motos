from flask import Flask, session
import os

from routes.auth_routes import auth
from routes.produto_routes import produto
from routes.moto_routes import moto
from routes.ordem_routes import ordem
from routes.usuario_routes import usuario

from repositories.notificacao_repository import contar_nao_lidas

# =========================
# APP FLASK
# =========================
app = Flask(__name__)
app.secret_key = "segredo123"

# =========================
# UPLOAD DE IMAGENS
# =========================
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB

# =========================
# BLUEPRINTS
# =========================
app.register_blueprint(auth)
app.register_blueprint(produto)
app.register_blueprint(moto)
app.register_blueprint(ordem)
app.register_blueprint(usuario)

# =========================
# CONTEXTO DO MENU (NOTIFICAÇÕES)
# =========================
@app.context_processor
def notificacoes_menu():
    if "usuario" in session:
        try:
            return {
                "total_notificacoes": contar_nao_lidas(session["usuario"])
            }
        except:
            return {"total_notificacoes": 0}

    return {"total_notificacoes": 0}
# =========================
# HOME ROUTE (opcional, evita erro de rota vazia)
# =========================
@app.route("/")
def home():
    return "SGO-Motos rodando 🚀"

# =========================
# INICIAR APP
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )