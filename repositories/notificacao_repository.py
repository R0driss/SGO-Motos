from database import conectar


def criar_notificacao(
    usuario,
    mensagem,
    data
):

    conn = conectar()

    conn.execute(

        """
        INSERT INTO notificacoes(
            usuario,
            mensagem,
            data
        )

        VALUES (?, ?, ?)
        """,

        (
            usuario,
            mensagem,
            data
        )

    )

    conn.commit()

    conn.close()


def listar_notificacoes(usuario):

    conn = conectar()

    notificacoes = conn.execute(

        """
        SELECT *
        FROM notificacoes
        WHERE usuario = ?
        ORDER BY id DESC
        """,

        (usuario,)

    ).fetchall()

    conn.close()

    return notificacoes


def contar_nao_lidas(usuario):

    conn = conectar()

    total = conn.execute(

        """
        SELECT COUNT(*) AS total
        FROM notificacoes
        WHERE usuario = ?
        AND lida = 0
        """,

        (usuario,)

    ).fetchone()

    conn.close()

    return total["total"]


def marcar_como_lida(usuario):

    conn = conectar()

    conn.execute(

        """
        UPDATE notificacoes

        SET lida = 1

        WHERE usuario = ?
        """,

        (usuario,)

    )

    conn.commit()

    conn.close()