import os
import psycopg2
from psycopg2.extras import RealDictCursor

def conectar():

    conn = psycopg2.connect(
        host="db.rhdwmrhusrnvdlxqawht.supabase.co",
        database="postgres",
        user="postgres",
        password=os.getenv("DB_PASSWORD"),
        port=5432,
        sslmode="require",
        cursor_factory=RealDictCursor,
        connect_timeout=20
    )

    return conn