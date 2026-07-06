from flask import Blueprint, render_template, request, redirect, url_for, session

from services.usuario_service import *

auth = Blueprint("auth", __name__)

# =========================
# CADASTRO
# =========================

@auth.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]

        telefone = request.form["telefone"]

        email = request.form["email"]

        usuario = request.form["usuario"]

        senha = request.form["senha"]

        cadastro = cadastrar_usuario(
            nome,
            telefone,
            email,
            usuario,
            senha
        )

        if not cadastro:

            return "Usuário já existe"

        return redirect(url_for("auth.login"))

    return render_template("cadastro.html")

# =========================
# LOGIN
# =========================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        senha = request.form["senha"]

        user = login_usuario(
            usuario,
            senha
        )

        print("USER:", user)
        print("TIPO:", type(user))

        if user:

            session["usuario"] = user["usuario"]
            session["tipo"] = user["tipo"]

            print("TIPO USUARIO:", user["tipo"])

            if user["tipo"] == "admin":
                print("ENTROU COMO ADMIN")
                return redirect(url_for("produto.admin"))

            print("ENTROU COMO CLIENTE")
            return redirect(url_for("moto.cliente"))

        return "Login inválido"
    
    

    return render_template("login.html")

  # =========================
# ESQUECI SENHA
# =========================

@auth.route("/esqueci-senha")
def esqueci_senha():

    return render_template(
        "esqueci_senha.html"
    )

@auth.route("/enviar-recuperacao", methods=["POST"])
def enviar_recuperacao():

    email = request.form["email"]

    usuario = obter_usuario_por_email(email)

    if usuario:
        return "Usuário encontrado!"

    return "E-mail não encontrado!"
# =========================
# LOGOUT
# =========================

@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("produto.inicio"))