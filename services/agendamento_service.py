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
        FROM ordens
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
        INSERT INTO ordens
        (
            usuario,
            cliente,
            moto,
            servico,
            valor,
            status,
            data,
            horario
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            usuario,
            usuario,
            "-",
            servico,
            0,
            "Em andamento",
            data,
            horario
        )
    )

    conn.commit()
    conn.close()

    return True


def listar_agendamentos():

    conn = conectar()

    ordens = conn.execute(
        """
        SELECT *
        FROM ordens
        ORDER BY data, horario
        """
    ).fetchall()

    conn.close()

    return ordens


def confirmar_agendamento(id):

    conn = conectar()

    conn.execute(
        """
        UPDATE ordens
        SET status='Em andamento'
        WHERE id=?
        """,
        (id,)
    )

    conn.commit()
    conn.close()


def cancelar_agendamento(id):

    conn = conectar()

    conn.execute(
        """
        UPDATE ordens
        SET status='Cancelado'
        WHERE id=?
        """,
        (id,)
    )

    conn.commit()
    conn.close()