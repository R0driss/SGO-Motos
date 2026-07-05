from repositories.notificacao_repository import *

from datetime import datetime


def nova_notificacao(
    usuario,
    mensagem
):

    data = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    criar_notificacao(
        usuario,
        mensagem,
        data
    )


def minhas_notificacoes(usuario):

    return listar_notificacoes(
        usuario
    )


def quantidade_notificacoes(usuario):

    return contar_nao_lidas(
        usuario
    )


def ler_notificacoes(usuario):

    marcar_como_lida(
        usuario
    )