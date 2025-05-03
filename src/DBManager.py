import os
from typing import List, Optional

import psycopg2
from dotenv import load_dotenv

from src.database import CreatureDataBase

load_dotenv()
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")
port = os.getenv("DATABASE_PORT")


class DBManager(CreatureDataBase):
    """
    Класс для взаимодействия с БД.
    """

    def __init__(
        self, db_name: str, user: str, password: str, host: str, port: str
    ) -> None:
        """
        Метод инициализации класса.
        """
        super().__init__(db_name, user, password, host, port)
        self.db_config = {
            "dbname": db_name,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }

        self.connection = psycopg2.connect(**self.db_config)
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self) -> List:
        """метод получает список компаний и количество их вакансий."""
        query = """
        SELECT e.name, COUNT(v.id) AS vacancies_count 
        FROM employers e 
        LEFT JOIN vacancies v ON e.id = v.employer_id 
        GROUP BY e.id;
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> List:
        """Метод получает все вакансии из базы данных."""
        query = """
        SELECT e.name AS company_name, v.title AS vacancy_title, v.salary_min AS min_salary,
               v.salary_max AS max_salary 
        FROM vacancies v 
        JOIN employers e ON v.employer_id = e.id;
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """метод получает среднюю зарплату по всем вакансиям."""
        query = "SELECT AVG((salary_min + salary_max) / 2) FROM vacancies;"

        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List:
        """метод получает все вакансии с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()

        query = """
          SELECT * FROM vacancies WHERE (salary_min + salary_max) / 2 > %s;
          """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List:
        """метод получает все вакансии по ключевому слову"""
        query = "SELECT * FROM vacancies WHERE name LIKE %s;"
        self.cursor.execute(query, ("%" + keyword + "%",))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
