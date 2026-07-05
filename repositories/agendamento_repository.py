from database import conectar

def criar_agendamento(
    usuario,
    servico,
    data,
    horario
):

    conn = conectar()

    existe = conn.execute(
        """
        SELECT *
        FROM agendamentos
        WHERE data = ?
        AND horario = ?
        AND status != 'Cancelado'
        """,
        (data, horario)
    ).fetchone()

    if existe:

        conn.close()

        return False

    conn.execute(
        """
        INSERT INTO agendamentos
        (
            usuario,
            servico,
            data,
            horario,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            usuario,
            servico,
            data,
            horario,
            "Pendente"
        )
    )

    conn.commit()
    conn.close()

    return True