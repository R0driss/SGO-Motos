from repositories.ordem_repository import (
    listar_ordens_admin,
    listar_ordens_usuario,
    adicionar_ordem,
    finalizar_ordem,
    remover_ordem,
    buscar_ordens,
    alterar_status,
    buscar_ordem_por_id
)

def obter_ordem(id):

    return buscar_ordem_por_id(id)