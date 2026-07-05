from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    make_response
)

import openpyxl
from io import BytesIO
from weasyprint import HTML
from repositories.ordem_repository import atualizar_valor_ordem
from services.notificacao_service import nova_notificacao
from services.ordem_service import *
from services.notificacao_service import nova_notificacao

ordem = Blueprint("ordem", __name__)

# =========================
# ORDENS
# =========================

@ordem.route("/ordens")
def ordens():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session["tipo"] == "admin":
        ordens = listar_ordens_admin()
    else:
        ordens = listar_ordens_usuario(session["usuario"])

    return render_template("ordens.html", ordens=ordens)


# =========================
# HISTÓRICO
# =========================

@ordem.route("/historico_ordens")
def historico_ordens():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    cliente = request.args.get("cliente", "")
    moto_busca = request.args.get("moto", "")
    servico = request.args.get("servico", "")
    status = request.args.get("status", "")

    ordens = buscar_ordens(
        cliente,
        moto_busca,
        servico,
        status
    )

    return render_template(
        "historico_ordens.html",
        ordens=ordens
    )


# =========================
# PDF
# =========================

@ordem.route("/historico_ordens/pdf")
def historico_ordens_pdf():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    ordens = buscar_ordens(
        request.args.get("cliente", ""),
        request.args.get("moto", ""),
        request.args.get("servico", ""),
        request.args.get("status", "")
    )

    html = render_template(
        "historico_ordens.html",
        ordens=ordens,
        pdf=True
    )

    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=historico_ordens.pdf"

    return response


# =========================
# EXCEL
# =========================

@ordem.route("/historico_ordens/excel")
def historico_ordens_excel():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    ordens = buscar_ordens(
        request.args.get("cliente", ""),
        request.args.get("moto", ""),
        request.args.get("servico", ""),
        request.args.get("status", "")
    )

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Historico de Ordens"

    sheet.append(["ID", "Cliente", "Serviço", "Valor", "Status"])

    for o in ordens:
        sheet.append([
            o["id"],
            o["cliente"],
            o["servico"],
            o["valor"],
            o["status"]
        ])

    arquivo = BytesIO()
    workbook.save(arquivo)
    arquivo.seek(0)

    response = make_response(arquivo.read())
    response.headers["Content-Disposition"] = "attachment; filename=historico_ordens.xlsx"
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return response


# =========================
# ADICIONAR ORDEM (ADMIN)
# =========================

@ordem.route("/adicionar_ordem", methods=["POST"])
def adicionar_ordem_admin():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session["tipo"] != "admin":
        return "Acesso negado"

    adicionar_ordem(
        request.form["usuario"],
        request.form["cliente"],
        request.form["moto"],
        request.form["servico"],
        request.form["valor"]
    )

    return redirect(url_for("ordem.ordens"))


# =========================
# FINALIZAR
# =========================

@ordem.route("/finalizar_ordem/<int:id>")
def finalizar_ordem_admin(id):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session["tipo"] != "admin":
        return "Acesso negado"

    finalizar_ordem(id)

    return redirect(url_for("ordem.ordens"))


# =========================
# REMOVER
# =========================

@ordem.route("/remover_ordem/<int:id>")
def remover_ordem_admin(id):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session["tipo"] != "admin":
        return "Acesso negado"

    remover_ordem(id)

    return redirect(url_for("ordem.ordens"))


# =========================
# STATUS
# =========================

@ordem.route(
    "/alterar_status/<int:id>/<status>"
)
def alterar_status_ordem(id, status):

    if "usuario" not in session:

        return redirect(
            url_for("auth.login")
        )

    if session["tipo"] != "admin":

        return "Acesso negado"

    # Busca a ordem
    ordem = obter_ordem(id)

    # Atualiza o status
    alterar_status(
        id,
        status
    )

    # Cria a mensagem
    if status == "Em andamento":

        mensagem = "🔧 Sua ordem entrou em andamento."

    elif status == "Concluido":

        mensagem = "✅ Sua ordem foi concluída."

    elif status == "Cancelado":

        mensagem = "❌ Sua ordem foi cancelada."

    else:

        mensagem = f"O status da sua ordem foi alterado para {status}."

    # Salva a notificação
    nova_notificacao(
        ordem["usuario"],
        mensagem
    )

    return redirect(
        "/historico_ordens"
    )

# =========================
# EDITAR VALOR
# =========================

@ordem.route("/atualizar_valor/<int:id>", methods=["POST"])
def atualizar_valor(id):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session["tipo"] != "admin":
        return "Acesso negado"

    valor = request.form["valor"]

    atualizar_valor_ordem(id, valor)

    return redirect(url_for("ordem.historico_ordens"))