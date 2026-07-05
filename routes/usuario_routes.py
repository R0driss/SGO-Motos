from flask import Blueprint, render_template, request, redirect, url_for, session

from services.usuario_service import *
from services.notificacao_service import *
usuario = Blueprint("usuario", __name__)

# =========================
# USUÁRIOS
# =========================

@usuario.route("/usuarios")
def usuarios():

    if "usuario" not in session:

        return redirect(url_for("auth.login"))

    if session["tipo"] != "admin":

        return "Acesso negado"

    busca = request.args.get("busca")

    usuarios = listar_usuarios(busca)

    return render_template(
        "usuarios.html",
        usuarios=usuarios
    )
# =========================
# PERFIL
# =========================

@usuario.route("/perfil", methods=["GET", "POST"])
def perfil():

    if "usuario" not in session:

        return redirect(url_for("auth.login"))

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        senha = request.form["senha"]

        salvar_usuario(
            session["usuario"],
            nome,
            email,
            telefone,
            senha
        )

        return redirect("/perfil")

    usuario_dados = obter_usuario(
        session["usuario"]
    )

    return render_template(
        "perfil.html",
        usuario=usuario_dados
    )

# =========================
# NOTIFICAÇÕES
# =========================

@usuario.route("/notificacoes")
def notificacoes():

    if "usuario" not in session:

        return redirect(
            url_for("auth.login")
        )

    ler_notificacoes(
        session["usuario"]
    )

    notificacoes = minhas_notificacoes(
        session["usuario"]
    )

    return render_template(
        "notificacoes.html",
        notificacoes=notificacoes
    )