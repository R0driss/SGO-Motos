from database import conectar


def listar_motos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM motos ORDER BY id DESC"
    )

    motos = cursor.fetchall()

    cursor.close()
    conn.close()

    return motos


def listar_motos_usuario(usuario):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM motos
        WHERE usuario = %s
        ORDER BY id DESC
        """,
        (usuario,)
    )

    motos = cursor.fetchall()

    cursor.close()
    conn.close()

    return motos


def registrar_moto(
    usuario,
    modelo,
    marca,
    placa,
    ano,
    problema,
    foto
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO motos (
            usuario,
            modelo,
            marca,
            placa,
            ano,
            problema,
            foto
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            usuario,
            modelo,
            marca,
            placa,
            ano,
            problema,
            foto
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


def remover_moto(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM motos WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()