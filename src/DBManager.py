import psycopg2

from typing import List, Optional, Tuple


class DBManager:
    def __init__(self, db_config):
        """Инициализация DBManager и подключение к базе данных."""
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def create_tables(self) -> None:
        """Создает таблицы employers и vacancies в базе данных, если они не существуют."""
        create_employers_table = """
        DROP TABLE employers IF EXISTS
        CREATE TABLE employers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            vacancies_count INTEGER DEFAULT 0
        );
        """

        create_vacancies_table = """
        DROP TABLE vacancies IF EXISTS
        CREATE TABLE vacancies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            salary_min INTEGER,
            salary_max INTEGER,
            employer_id INTEGER REFERENCES employers(id)
        );
        """

        self.cursor.execute(create_employers_table)
        self.cursor.execute(create_vacancies_table)
        self.connection.commit()

    def insert_employer(self, name: str) -> int:
        """Метод вставляет нового работодателя в таблицу employers."""
        self.cursor.execute(
            "INSERT INTO employers (name) VALUES (%s) RETURNING id;", (name,)
        )
        employer_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return employer_id

    def insert_vacancy(
            self,
            name: str,
            salary_min: Optional[int],
            salary_max: Optional[int],
            employer_id: int,
    ) -> None:
        """метод вставляет новую вакансию в таблицу vacancies."""

        self.cursor.execute(
            "INSERT INTO vacancies (name, salary_min, salary_max, employer_id) VALUES (%s, %s, %s, %s);",
            (name, salary_min, salary_max, employer_id),
        )
        self.connection.commit()

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


if __name__ == '__main__':
    db_config = {'host': 'localhost',
                 'database': 'my DT',
                 'user': 'postgres',
                 'password': 'Al.krotov7'}
    DBManager.create_tables(db_config)
