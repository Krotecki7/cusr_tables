import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
user = os.getenv('DATABASE_USER')
password = os.getenv('DATABASE_PASSWORD')
host = os.getenv('DATABASE_HOST')
port = os.getenv('DATABASE_PORT')


class CreatureDataBase:
    """
    Класс для автоматического создания базы данных PostgreSQL.
    """
    db_name: str
    user: str
    password: str
    host: str
    port: str

    def __init__(self, db_name: str, user: str, password: str, host: str, port: str) -> None:
        """
        Метод инициализации класса
        """
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
