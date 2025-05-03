import os
from typing import Any

import psycopg2
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")
port = os.getenv("DATABASE_PORT")


class CreatureDataBase:
    """
    Класс для автоматического создания базы данных PostgreSQL.
    """

    db_name: str
    user: str
    password: str
    host: str
    port: str

    def __init__(
        self, db_name: str, user: str, password: str, host: str, port: str
    ) -> None:
        """
        Метод инициализации класса
        """
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect_bd(self) -> None:
        """
        Метод для подключения к базе данных PostgreSQL.
        """
        conn = None
        try:
            print(self.port)
            conn = psycopg2.connect(
                dbname="hh_tables",
                user=self.user,
                password=self.password,
                host=self.host,
                port=int(self.port),
            )
            conn.autocommit = True

            cur = conn.cursor()

            cur.execute(
                """SELECT 1 FROM pg_database WHERE datname LIKE %s""",
                (f"%{self.db_name}%",),
            )
            exists = cur.fetchone()
            if exists:
                print(f"База данных '{self.db_name}' уже существует.")
                cur.execute(f"DROP DATABASE {self.db_name}")
                print(f"База данных '{self.db_name}' успешно удалена.")

            print(f"Создаём базу данных '{self.db_name}'...")
            cur.execute(f"CREATE DATABASE {self.db_name}")
            print(f"База данных '{self.db_name}' успешно создана.")

            cur.close()

        except psycopg2.Error as e:
            print(f"Ошибка при создании базы данных '{self.db_name}': {e}")

        finally:
            if conn:
                conn.close()
                print("Соединение с PostgreSQL закрыто.")

    def employees_table(self) -> None:
        """
        Метод создания таблицы компаний в БД.
        """
        with psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=int(self.port),
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS employees (employee_id int PRIMARY KEY, "
                    "employee_name varchar(100) NOT NULL)"
                )
                conn.commit()
                cur.execute("SELECT * FROM employees")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        conn.close()

    def vacancies_table(self) -> None:
        """
        Метод создания таблицы вакансий в БД.
        """
        with psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=int(self.port),
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS vacancies (vacancy_id int PRIMARY KEY, employee_id int NOT NULL, "
                    "vacancy_title varchar(255) NOT NULL, salary_from int, salary_to int, "
                    "vacancy_url varchar(255) NOT NULL, "
                    "FOREIGN KEY (employee_id) REFERENCES employees(employee_id))"
                )
                conn.commit()
                cur.execute("SELECT * FROM vacancies")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        conn.close()

    def insert_employees(self, employer: Any) -> None:
        """
        Метод заполнения данными таблицы компаний в БД.
        """
        with psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=int(self.port),
        ) as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        """ INSERT INTO employees (employee_id, employee_name) VALUES (%s, %s);""",
                        (employer["id"], employer["name"]),
                    )
                    conn.commit()
                except Exception as e:
                    print(f"Ошибка при вставке компании {e}")
        conn.close()

    def insert_vacancies(self, vacancy: Any, employee_id: Any) -> None:
        """
        Метод заполнения данными таблицы вакансий в БД.
        """
        with psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=int(self.port),
        ) as conn:
            with conn.cursor() as cur:
                try:
                    vacancy_id = int(vacancy["id"])
                    employee_id = int(employee_id)
                    salary = vacancy.get("salary")
                    salary_from = salary.get("from") if salary else None
                    salary_to = salary.get("to") if salary else None

                    salary_from = int(salary_from) if salary_from is not None else None
                    salary_to = int(salary_to) if salary_to is not None else None

                    cur.execute(
                        """INSERT INTO vacancies (vacancy_id, employee_id, vacancy_title, salary_from,
                    salary_to, vacancy_url) VALUES (%s, %s, %s, %s, %s, %s)""",
                        (
                            vacancy_id,
                            employee_id,
                            vacancy["name"],
                            salary_from,
                            salary_to,
                            vacancy["alternate_url"],
                        ),
                    )
                    conn.commit()
                except Exception as e:
                    print(f"Ошибка при вставке вакансии {e}")
        conn.close()
