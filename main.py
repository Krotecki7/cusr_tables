from src.DBManager import DBManager


def main(user_manager):

    while True:
        print("1. Показать компании и количество вакансий")
        print("2. Показать среднюю зарплату")
        print("3. Показать вакансии по ключевому слову")
        print("4. Показать вакансии с зарплатой выше средней")

        choice = input("Выберите опцию (или 'exit' для выхода): ")

        if choice == "1":
            companies = user_manager.get_companies_and_vacancies_count()
            if companies:
                for company in companies:
                    print(f"Компания: {company[0]}, Вакансий: {company[1]}")
            else:
                print("Нет доступных компаний.")

        elif choice == "2":
            avg_salary = user_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")

        elif choice == "3":
            keyword = input("Введите ключевое слово: ")
            keyword_vacancies = user_manager.get_vacancies_with_keyword(keyword)
            if keyword_vacancies:
                for vacancy in keyword_vacancies:
                    print(vacancy)
            else:
                print(f"Нет вакансий по ключевому слову '{keyword}'.")
        elif choice == "4":
            higher_salary_vacancies = user_manager.get_vacancies_with_higher_salary()
            for vacancy in higher_salary_vacancies:
                print(vacancy)

        elif choice.lower() == "exit":
            break


if __name__ == '__main__':
    main(user_manager=DBManager('my DT'))
