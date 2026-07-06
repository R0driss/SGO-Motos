from database import conectar


def criar_agendamento(
    usuario,
    servico,
    data,
    horario
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM agendamentos
        WHERE data = %s
        AND horario = %s
        AND status != 'Cancelado'
        """,
        (data, horario)
    )

    existe = cursor.fetchone()

    if existe:

        cursor.close()
        conn.close()

        return False

    cursor.execute(
        """
        INSERT INTO agendamentos
        (
            usuario,
            servico,
            data,
            horario,
            status
        )
        VALUES (%s, %s, %s, %s, %s)
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

    cursor.close()
    conn.close()

    return True