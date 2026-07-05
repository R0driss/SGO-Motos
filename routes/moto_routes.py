from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import os
from werkzeug.utils import secure_filename

from services.moto_service import *
from services.produto_service import *
from services.ordem_service import adicionar_ordem
from services.notificacao_service import nova_notificacao

moto = Blueprint("moto", __name__)

UPLOAD_FOLDER = "static/uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# =========================
# CLIENTE
# =========================

@moto.route("/cliente")
def cliente():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    produtos = listar_produtos()

    motos = listar_motos_usuario(session["usuario"])

    return render_template(
        "cliente.html",
        produtos=produtos,
        motos=motos
    )

# =========================
# REGISTRAR MOTO
# =========================

@moto.route("/registrar_moto", methods=["POST"])
def registrar_moto_post():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    usuario = session["usuario"]

    modelo = request.form["modelo"]
    marca = request.form["marca"]
    placa = request.form["placa"]
    ano = request.form["ano"]
    problema = request.form["problema"]

    fotos = request.files.getlist("fotos")

    nomes_arquivos = []

    for foto in fotos:

        if foto.filename != "":

            nome_arquivo = secure_filename(foto.filename)

            caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)

            foto.save(caminho)

            nomes_arquivos.append(nome_arquivo)

    fotos_texto = ",".join(nomes_arquivos)

    # salva moto
    registrar_moto(
        usuario,
        modelo,
        marca,
        placa,
        ano,
        problema,
        fotos_texto
    )

    # cria ordem automaticamente
    adicionar_ordem(
        usuario,
        usuario,
        f"{marca} {modelo} - {placa}",
        problema,
        0
    )
    nova_notificacao(
    "admin",
    f"""NOVA ORDEM DE SERVIÇO


Cliente : {usuario} ,
Moto    : {marca} - {modelo},
Placa   : {placa},
Serviço : {problema}

"""
)
    

    return redirect("/cliente")


# =========================
# MOTOS ADMIN
# =========================

@moto.route("/motos")
def motos():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session.get("tipo") != "admin":
        return "Acesso negado"

    motos = listar_motos()

    return render_template(
        "motos.html",
        motos=motos
    )


# =========================
# REMOVER MOTO
# =========================

@moto.route("/remover_moto/<int:id>")
def remover_moto_admin(id):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session.get("tipo") != "admin":
        return "Acesso negado"

    remover_moto(id)

    return redirect(url_for("moto.motos"))


# =========================
# ADMIN
# =========================

@moto.route("/admin")
def admin():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session.get("tipo") != "admin":
        return "Acesso negado"

    produtos = listar_produtos()

    total_produtos = len(produtos)

    valor_total = sum(
        p.preco * p.quantidade
        for p in produtos
    )

    return render_template(
        "admin.html",
        produtos=produtos,
        total_produtos=total_produtos,
        valor_total=valor_total
    )