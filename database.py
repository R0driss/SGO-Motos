import os
import psycopg2

def conectar():
    url = os.getenv("DATABASE_URL")

    if not url:
        raise Exception("DATABASE_URL não configurada")

    # Corrige schema antigo do Heroku/Supabase
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    return psycopg2.connect(
        url,
        sslmode="require"
    )