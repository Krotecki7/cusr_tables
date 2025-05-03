from typing import Any, Dict, List

import requests


class APIManager:
    BASE_URL = "https://api.hh.ru"

    employs_id = [
        9140614,
        11099814,
        11674968,
        11747243,
        11826459,
        5004072,
        5775464,
        4748227,
        36227,
        3643187,
    ]

    @staticmethod
    def get_companies(employs_id: List[int]) -> List[Dict[str, Any]]:
        """метод получает информацию о компаниях по их идентификаторам."""
        companies = []
        for company_id in employs_id:
            response = requests.get(f"{APIManager.BASE_URL}/employers/{company_id}")
            if response.status_code == 200:
                companies.append(response.json())
            else:
                print(
                    f"Ошибка при получении компании с ID {company_id}: {response.status_code}"
                )
        return companies

    @staticmethod
    def get_vacancies(company_id: int) -> List[Dict[str, Any]]:
        """метод получает список вакансий для заданной компании."""
        response = requests.get(
            f"{APIManager.BASE_URL}/vacancies?employer_id={company_id}"
        )
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(
                f"Ошибка при получении вакансий для компании с ID {company_id}: {response.status_code}"
            )
            return []
