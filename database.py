import os
import psycopg2
import socket
from psycopg2.extras import RealDictCursor

def conectar():

    # força uso de IPv4
    socket.setdefaulttimeout(10)

    conn = psycopg2.connect(
        host="db.rhdwmrhusrnvdlxqawht.supabase.co",
        database="postgres",
        user="postgres",
        password=os.getenv("DB_PASSWORD"),
        port=5432,
        sslmode="require",
        cursor_factory=RealDictCursor,
        connect_timeout=10
    )

    return conn