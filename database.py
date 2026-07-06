import os
import psycopg2
import psycopg2.extras

def conectar():
    url = os.getenv("DATABASE_URL")

    if not url:
        raise Exception("DATABASE_URL não configurada")

    url = url.replace("postgres://", "postgresql://", 1)

    conn = psycopg2.connect(url, sslmode="require")
    conn.cursor_factory = psycopg2.extras.RealDictCursor

    return conn