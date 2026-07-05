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