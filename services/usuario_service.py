import secrets
from datetime import datetime, timedelta
from repositories.usuario_repository import *

from services.email_service import enviar_email

def cadastrar_usuario(
    nome,
    telefone,
    email,
    usuario,
    senha
):

    existe = buscar_usuario_existente(usuario)

    if existe:

        return False

    criar_usuario(
        usuario,
        senha,
        "cliente",
        nome,
        telefone,
        email
    )

    enviar_email(
        nome,
        usuario,
        email
    )

    return True


def login_usuario(
    usuario,
    senha
):

    return buscar_usuario(
        usuario,
        senha
    )

def obter_usuario(usuario):

    return buscar_usuario_por_login(
        usuario
    )


def salvar_usuario(
    usuario,
    nome,
    email,
    telefone,
    senha
):

    atualizar_usuario(
        usuario,
        nome,
        email,
        telefone,
        senha
    )


def obter_usuario_por_email(email):

    return buscar_usuario_por_email(
        email
    )

def gerar_token():

    return secrets.token_urlsafe(32)

def criar_token_recuperacao(email):

    print("1 - Entrou na função")

    usuario = buscar_usuario_por_email(email)
    print("2 - Usuário:", usuario)

    if not usuario:
        print("3 - Usuário não encontrado")
        return None

    token = gerar_token()
    print("4 - Token:", token)

    expiracao = datetime.now() + timedelta(minutes=30)
    print("5 - Expiração:", expiracao)

    salvar_token_recuperacao(
        email,
        token,
        expiracao
    )

    print("6 - Token salvo no banco")

    return token