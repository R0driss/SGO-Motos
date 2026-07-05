from database import conectar

def listar_motos():

    conn = conectar()

    motos = conn.execute(

        "SELECT * FROM motos ORDER BY id DESC"

    ).fetchall()

    conn.close()

    return motos


def listar_motos_usuario(usuario):

    conn = conectar()

    motos = conn.execute(

        "SELECT * FROM motos WHERE usuario = ?",

        (usuario,)

    ).fetchall()

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

    conn.execute(

        """
        INSERT INTO motos(
            usuario,
            modelo,
            marca,
            placa,
            ano,
            problema,
            foto
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
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

    conn.close()

def remover_moto(id):

    conn = conectar()

    conn.execute(

        "DELETE FROM motos WHERE id = ?",

        (id,)

    )

    conn.commit()

    conn.close()