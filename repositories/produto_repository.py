from database import conectar


def listar_produtos(busca=None):

    conn = conectar()
    cursor = conn.cursor()

    if busca:

        cursor.execute(

            "SELECT * FROM produtos WHERE nome ILIKE %s",

            (f"%{busca}%",)

        )

    else:

        cursor.execute(

            "SELECT * FROM produtos"

        )

    produtos = cursor.fetchall()

    cursor.close()
    conn.close()

    return produtos


def adicionar_produto(
    nome,
    quantidade,
    preco
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(

        "INSERT INTO produtos(nome, quantidade, preco) VALUES (%s, %s, %s)",

        (nome, quantidade, preco)

    )

    conn.commit()

    cursor.close()
    conn.close()


def remover_produto(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM produtos WHERE id = %s",

        (id,)

    )

    conn.commit()

    cursor.close()
    conn.close()


def aumentar_produto(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(

        "UPDATE produtos SET quantidade = quantidade + 1 WHERE id = %s",

        (id,)

    )

    conn.commit()

    cursor.close()
    conn.close()


def diminuir_produto(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM produtos WHERE id = %s",

        (id,)

    )

    produto = cursor.fetchone()

    if produto and produto["quantidade"] > 0:

        cursor.execute(

            "UPDATE produtos SET quantidade = quantidade - 1 WHERE id = %s",

            (id,)

        )

        conn.commit()

    cursor.close()
    conn.close()