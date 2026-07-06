import os
import psycopg2

def conectar():
    url = os.environ.get("DATABASE_URL")

    if not url:
        raise Exception("DATABASE_URL não configurada")

    return psycopg2.connect(url)