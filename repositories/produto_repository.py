from database import conectar

def listar_produtos(busca=None):

    conn = conectar()

    if busca:

        produtos = conn.execute(

            "SELECT * FROM produtos WHERE nome LIKE ?",

            (f"%{busca}%",)

        ).fetchall()

    else:

        produtos = conn.execute(

            "SELECT * FROM produtos"

        ).fetchall()

    conn.close()

    return produtos


def adicionar_produto(
    nome,
    quantidade,
    preco
):

    conn = conectar()

    conn.execute(

        "INSERT INTO produtos(nome, quantidade, preco) VALUES (?, ?, ?)",

        (nome, quantidade, preco)

    )

    conn.commit()

    conn.close()


def remover_produto(id):

    conn = conectar()

    conn.execute(

        "DELETE FROM produtos WHERE id = ?",

        (id,)

    )

    conn.commit()

    conn.close()


def aumentar_produto(id):

    conn = conectar()

    conn.execute(

        "UPDATE produtos SET quantidade = quantidade + 1 WHERE id = ?",

        (id,)

    )

    conn.commit()

    conn.close()


def diminuir_produto(id):

    conn = conectar()

    produto = conn.execute(

        "SELECT * FROM produtos WHERE id = ?",

        (id,)

    ).fetchone()

    if produto["quantidade"] > 0:

        conn.execute(

            "UPDATE produtos SET quantidade = quantidade - 1 WHERE id = ?",

            (id,)

        )

        conn.commit()

    conn.close()