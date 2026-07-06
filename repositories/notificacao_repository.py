from database import conectar


def criar_notificacao(
    usuario,
    mensagem,
    data
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO notificacoes(
            usuario,
            mensagem,
            data
        )
        VALUES (%s, %s, %s)
        """,
        (
            usuario,
            mensagem,
            data
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


def listar_notificacoes(usuario):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM notificacoes
        WHERE usuario = %s
        ORDER BY id DESC
        """,
        (usuario,)
    )

    notificacoes = cursor.fetchall()

    cursor.close()
    conn.close()

    return notificacoes


def contar_nao_lidas(usuario):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM notificacoes
        WHERE usuario = %s
        AND lida = FALSE
        """,
        (usuario,)
    )

    total = cursor.fetchone()

    cursor.close()
    conn.close()

    return total["total"]


def marcar_como_lida(usuario):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE notificacoes
        SET lida = TRUE
        WHERE usuario = %s
        """,
        (usuario,)
    )

    conn.commit()

    cursor.close()
    conn.close()