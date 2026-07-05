from flask import Blueprint, render_template, request, redirect, url_for, session, make_response
from weasyprint import HTML
import sqlite3
import openpyxl

from io import BytesIO
from services.produto_service import *

produto = Blueprint("produto", __name__)

# =========================
# INÍCIO
# =========================

@produto.route("/")
def inicio():

    busca = request.args.get("busca")

    produtos = listar_produtos(busca)

    return render_template(
        "index.html",
        produtos=produtos
    )

# =========================
# ADMIN
# =========================

@produto.route("/admin")
def admin():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session.get("tipo") != "admin":
        return "Acesso negado"

    produtos = listar_produtos()

    total_produtos = len(produtos)

    valor_total = sum(
        p["preco"] * p["quantidade"]
        for p in produtos
    )

    nomes = [
        p["nome"]
        for p in produtos
    ]

    quantidades = [
        p["quantidade"]
        for p in produtos
    ]

    return render_template(
        "admin.html",
        produtos=produtos,
        total_produtos=total_produtos,
        valor_total=valor_total,
        nomes=nomes,
        quantidades=quantidades
    )
# =========================
# RELATÓRIO DE ESTOQUE
# =========================

@produto.route("/relatorio_estoque")
def relatorio_estoque():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session["tipo"] != "admin":
        return "Acesso negado"

    produtos = listar_produtos()

    total_produtos = len(produtos)

    valor_total = 0

    sem_estoque = 0
    estoque_baixo = 0
    estoque_normal = 0
    estoque_alto = 0

    for p in produtos:

        valor_total += p["preco"] * p["quantidade"]

        if p["quantidade"] == 0:
            sem_estoque += 1

        elif p["quantidade"] <= 15:
            estoque_baixo += 1

        elif p["quantidade"] <= 50:
            estoque_normal += 1

        else:
            estoque_alto += 1

    return render_template(
        "relatorio_estoque.html",
        produtos=produtos,
        total_produtos=total_produtos,
        valor_total=valor_total,
        sem_estoque=sem_estoque,
        estoque_baixo=estoque_baixo,
        estoque_normal=estoque_normal,
        estoque_alto=estoque_alto
    )
@produto.route("/relatorio_estoque/pdf")
def relatorio_estoque_pdf():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session["tipo"] != "admin":
        return "Acesso negado"

    produtos = listar_produtos()

    total_produtos = len(produtos)

    valor_total = 0

    sem_estoque = 0
    estoque_baixo = 0
    estoque_normal = 0
    estoque_alto = 0

    for p in produtos:

        valor_total += p["preco"] * p["quantidade"]

        if p["quantidade"] == 0:
            sem_estoque += 1

        elif p["quantidade"] <= 15:
            estoque_baixo += 1

        elif p["quantidade"] <= 50:
            estoque_normal += 1

        else:
            estoque_alto += 1

    html = render_template(
        "relatorio_estoque.html",
        produtos=produtos,
        total_produtos=total_produtos,
        valor_total=valor_total,
        sem_estoque=sem_estoque,
        estoque_baixo=estoque_baixo,
        estoque_normal=estoque_normal,
        estoque_alto=estoque_alto
    )

    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)

    response.headers["Content-Type"] = "application/pdf"

    response.headers["Content-Disposition"] = (
        "attachment; filename=relatorio_estoque.pdf"
    )

    return response


@produto.route("/relatorio_estoque/excel")
def relatorio_estoque_excel():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session["tipo"] != "admin":
        return "Acesso negado"

    produtos = listar_produtos()

    workbook = openpyxl.Workbook()

    sheet = workbook.active

    sheet.title = "Relatório Estoque"

    # =========================
    # CABEÇALHO
    # =========================

    sheet.append([
        "Produto",
        "Quantidade",
        "Preço Unitário",
        "Valor em Estoque",
        "Status"
    ])

    # =========================
    # DADOS
    # =========================

    for produto in produtos:

        valor_estoque = (
            produto["preco"] *
            produto["quantidade"]
        )

        if produto["quantidade"] == 0:

            status = "Sem Estoque"

        elif produto["quantidade"] <= 15:

            status = "Estoque Baixo"

        elif produto["quantidade"] <= 50:

            status = "Estoque Normal"

        else:

            status = "Estoque Alto"

        sheet.append([

            produto["nome"],

            produto["quantidade"],

            f'R$ {produto["preco"]:.2f}',

            f'R$ {valor_estoque:.2f}',

            status
        ])

    # =========================
    # AJUSTAR LARGURA
    # =========================

    for coluna in sheet.columns:

        maior = 0

        letra_coluna = coluna[0].column_letter

        for celula in coluna:

            try:

                if len(str(celula.value)) > maior:

                    maior = len(str(celula.value))

            except:
                pass

        largura = maior + 5

        sheet.column_dimensions[
            letra_coluna
        ].width = largura

    # =========================
    # GERAR ARQUIVO
    # =========================

    arquivo = BytesIO()

    workbook.save(arquivo)

    arquivo.seek(0)

    response = make_response(
        arquivo.read()
    )

    response.headers[
        "Content-Disposition"
    ] = (
        "attachment; "
        "filename=relatorio_estoque.xlsx"
    )

    response.headers[
        "Content-type"
    ] = (
        "application/vnd.openxmlformats-"
        "officedocument.spreadsheetml.sheet"
    )

    return response


# =========================
# PRODUTOS
# =========================

@produto.route("/adicionar", methods=["POST"])
def adicionar():

    if session["tipo"] != "admin":
        return "Acesso negado"

    nome = request.form["nome"]

    quantidade = int(
        request.form["quantidade"]
    )

    preco = float(
        request.form["preco"]
    )

    adicionar_produto(
        nome,
        quantidade,
        preco
    )

    return redirect(url_for("produto.admin"))

@produto.route("/remover/<int:id>")
def remover(id):

    if session["tipo"] != "admin":
        return "Acesso negado"

    remover_produto(id)

    return redirect(url_for("produto.admin"))

@produto.route("/aumentar/<int:id>")
def aumentar(id):

    aumentar_produto(id)

    return redirect(url_for("produto.admin"))

@produto.route("/diminuir/<int:id>")
def diminuir(id):

    diminuir_produto(id)

    return redirect(url_for("produto.admin"))