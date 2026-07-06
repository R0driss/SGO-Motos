from database import conectar


def listar_ordens_admin():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM ordens ORDER BY id DESC"
    )

    ordens = cursor.fetchall()

    cursor.close()
    conn.close()

    return ordens


def listar_ordens_usuario(usuario):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM ordens
        WHERE usuario = %s
        ORDER BY id DESC
        """,
        (usuario,)
    )

    ordens = cursor.fetchall()

    cursor.close()
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
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ordens(
            usuario,
            cliente,
            moto,
            servico,
            valor,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
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

    cursor.close()
    conn.close()


def finalizar_ordem(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE ordens
        SET status = %s
        WHERE id = %s
        """,
        (
            "Finalizado",
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


def remover_ordem(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM ordens WHERE id = %s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()


def buscar_ordens(cliente="", moto="", servico="", status=""):

    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT * FROM ordens
        WHERE 1=1
    """

    parametros = []

    if cliente:
        query += " AND cliente ILIKE %s"
        parametros.append(f"%{cliente}%")

    if moto:
        query += " AND moto ILIKE %s"
        parametros.append(f"%{moto}%")

    if servico:
        query += " AND servico ILIKE %s"
        parametros.append(f"%{servico}%")

    if status:
        query += " AND status = %s"
        parametros.append(status)

    query += " ORDER BY id DESC"

    cursor.execute(query, tuple(parametros))

    ordens = cursor.fetchall()

    cursor.close()
    conn.close()

    return ordens


def alterar_status(id, status):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE ordens
        SET status = %s
        WHERE id = %s
        """,
        (
            status,
            id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


def atualizar_valor_ordem(id, valor):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE ordens
        SET valor = %s
        WHERE id = %s
        """,
        (valor, id)
    )

    conn.commit()

    cursor.close()
    conn.close()


def buscar_ordem_por_id(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM ordens
        WHERE id = %s
        """,
        (id,)
    )

    ordem = cursor.fetchone()

    cursor.close()
    conn.close()

    return ordem