import os
import psycopg2

def conectar():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn