from database import conectar

def buscar_usuario(usuario, senha):

    conn = conectar()

    user = conn.execute(

        "SELECT * FROM usuarios WHERE usuario = ? AND senha = ?",

        (usuario, senha)

    ).fetchone()

    conn.close()

    return user


def buscar_usuario_existente(usuario):

    conn = conectar()

    existe = conn.execute(

        "SELECT * FROM usuarios WHERE usuario = ?",

        (usuario,)

    ).fetchone()

    conn.close()

    return existe


def criar_usuario(
    usuario,
    senha,
    tipo,
    nome,
    telefone,
    email
):

    conn = conectar()

    conn.execute(

        """

        INSERT INTO usuarios(
            usuario,
            senha,
            tipo,
            nome,
            telefone,
            email
        )

        VALUES (?, ?, ?, ?, ?, ?)

        """,

        (
            usuario,
            senha,
            tipo,
            nome,
            telefone,
            email
        )

    )

    conn.commit()

    conn.close()


def listar_usuarios(busca=None):

    conn = conectar()

    if busca:

        usuarios = conn.execute(

            """

            SELECT

                id,
                nome,
                usuario,
                email,
                telefone,
                tipo

            FROM usuarios

            WHERE nome LIKE ?

            ORDER BY id DESC

            """,

            (f"%{busca}%",)

        ).fetchall()

    else:

        usuarios = conn.execute(

            """

            SELECT

                id,
                nome,
                usuario,
                email,
                telefone,
                tipo

            FROM usuarios

            ORDER BY id DESC

            """

        ).fetchall()

    conn.close()

    return usuarios

def buscar_usuario_por_login(usuario):

    conn = conectar()

    usuario_encontrado = conn.execute(

        """
        SELECT *
        FROM usuarios
        WHERE usuario = ?
        """,

        (usuario,)

    ).fetchone()

    conn.close()

    return usuario_encontrado

def atualizar_usuario(
    usuario,
    nome,
    email,
    telefone,
    senha
):

    conn = conectar()

    conn.execute(

        """
        UPDATE usuarios

        SET
            nome = ?,
            email = ?,
            telefone = ?,
            senha = ?

        WHERE usuario = ?
        """,

        (
            nome,
            email,
            telefone,
            senha,
            usuario
        )

    )

    conn.commit()

    conn.close()