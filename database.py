import socket
socket.getaddrinfo = lambda *args, **kwargs: socket._socket.getaddrinfo(*args, **kwargs)
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def conectar():

    conn = psycopg2.connect(
        host="db.rhdwmrhusrnvdlxqawht.supabase.co",
        dbname="postgres",
        user="postgres",
        password=os.getenv("DB_PASSWORD"),
        port=5432,
        sslmode="require",
        connect_timeout=20,
        cursor_factory=RealDictCursor,
        options="-c client_encoding=UTF8"
    )

    return conn