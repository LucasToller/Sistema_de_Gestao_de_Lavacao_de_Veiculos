import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",           # >>> AJUSTAR AQUI  <<<
    "password": "sua_senha!",  # >>> AJUSTAR AQUI <<<
    "database": "lava_car"
}

def get_connection():
    """Abre uma conexão com o banco de dados lava_car."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Erro ao conectar no banco: {e}")
        return None