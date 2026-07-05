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

        if user:

            session["usuario"] = user["usuario"]

            session["tipo"] = user["tipo"]

            if user["tipo"] == "admin":

                return redirect(url_for("produto.admin"))

            return redirect(url_for("moto.cliente"))

        return "Login inválido"

    return render_template("login.html")

# =========================
# LOGOUT
# =========================

@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("produto.inicio"))