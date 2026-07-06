from database import conectar
from psycopg2.extras import RealDictCursor


def criar_admin():
    conn = conectar()
    conn.execute("""
        INSERT INTO usuarios (nome, email, senha, tipo)
        VALUES (%s, %s, %s, %s)
    """, ("Admin", "admin@admin.com", "123456", "admin"))
    conn.commit()
    conn.close()

from psycopg2.extras import RealDictCursor

def buscar_usuario(usuario, senha):

    conn = conectar()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT *
        FROM usuarios
        WHERE usuario = %s
        AND senha = %s
        """,
        (usuario, senha)
    )

    user = cursor.fetchone()

    print("RESULTADO:", user)

    cursor.close()
    conn.close()

    return user

def buscar_usuario_existente(usuario):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = %s",
        (usuario,)
    )

    existe = cursor.fetchone()

    cursor.close()
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
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO usuarios(
            usuario,
            senha,
            tipo,
            nome,
            telefone,
            email
        )
        VALUES (%s, %s, %s, %s, %s, %s)
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

    cursor.close()
    conn.close()


def listar_usuarios(busca=None):

    conn = conectar()
    cursor = conn.cursor()

    if busca:

        cursor.execute(
            """
            SELECT
                id,
                nome,
                usuario,
                email,
                telefone,
                tipo
            FROM usuarios
            WHERE nome ILIKE %s
            ORDER BY id DESC
            """,
            (f"%{busca}%",)
        )

    else:

        cursor.execute(
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
        )

    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return usuarios


def buscar_usuario_por_login(usuario):

    conn = conectar()

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT *
        FROM usuarios
        WHERE usuario = %s
        """,
        (usuario,)
    )

    usuario_encontrado = cursor.fetchone()

    cursor.close()
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
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET
            nome = %s,
            email = %s,
            telefone = %s,
            senha = %s
        WHERE usuario = %s
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

    cursor.close()
    conn.close()

from psycopg2.extras import RealDictCursor

def buscar_usuario_por_email(email):

    conn = conectar()

    cursor = conn.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute(
        """
        SELECT *
        FROM usuarios
        WHERE email = %s
        """,
        (email,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return usuario