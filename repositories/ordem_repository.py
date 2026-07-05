from database import conectar

def listar_ordens_admin():

    conn = conectar()

    ordens = conn.execute(

        "SELECT * FROM ordens ORDER BY id DESC"

    ).fetchall()

    conn.close()

    return ordens


def listar_ordens_usuario(usuario):

    conn = conectar()

    ordens = conn.execute(

        """

        SELECT * FROM ordens
        WHERE usuario = ?

        ORDER BY id DESC

        """,

        (usuario,)

    ).fetchall()

    conn.close()

    return ordens


def adicionar_ordem(
    usuario,
    cliente,
    moto,
    servico,
    valor
):

    conn = conectar()

    conn.execute(

        """

        INSERT INTO ordens(
            usuario,
            cliente,
            moto,
            servico,
            valor,
            status
        )

        VALUES (?, ?, ?, ?, ?, ?)

        """,

        (
            usuario,
            cliente,
            moto,
            servico,
            valor,
            "Em andamento"
        )

    )

    conn.commit()

    conn.close()


def finalizar_ordem(id):

    conn = conectar()

    conn.execute(

        """

        UPDATE ordens
        SET status = ?

        WHERE id = ?

        """,

        (
            "Finalizado",
            id
        )

    )

    conn.commit()

    conn.close()


def remover_ordem(id):

    conn = conectar()

    conn.execute(

        "DELETE FROM ordens WHERE id = ?",

        (id,)

    )

    conn.commit()

    conn.close()

def buscar_ordens(cliente="", moto="", servico="", status=""):

    conn = conectar()

    query = """
        SELECT * FROM ordens
        WHERE 1=1
    """

    parametros = []

    if cliente:
        query += " AND cliente LIKE ?"
        parametros.append(f"%{cliente}%")

    if moto:
        query += " AND moto LIKE ?"
        parametros.append(f"%{moto}%")

    if servico:
        query += " AND servico LIKE ?"
        parametros.append(f"%{servico}%")

    if status:
        query += " AND status = ?"
        parametros.append(status)

    query += " ORDER BY id DESC"

    ordens = conn.execute(
        query,
        parametros
    ).fetchall()

    conn.close()

    return ordens

def alterar_status(id, status):

    conn = conectar()

    conn.execute(
        """
        UPDATE ordens
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            id
        )
    )

    conn.commit()
    conn.close()

def atualizar_valor_ordem(id, valor):

    conn = conectar()

    conn.execute(
        """
        UPDATE ordens
        SET valor = ?
        WHERE id = ?
        """,
        (valor, id)
    )

    conn.commit()
    conn.close()

def atualizar_valor_ordem(id, valor):

    conn = conectar()

    conn.execute(
        """
        UPDATE ordens
        SET valor = ?
        WHERE id = ?
        """,
        (valor, id)
    )

    conn.commit()
    conn.close()

def buscar_ordem_por_id(id):

    conn = conectar()

    ordem = conn.execute(

        """
        SELECT *
        FROM ordens
        WHERE id = ?
        """,

        (id,)

    ).fetchone()

    conn.close()

    return ordem