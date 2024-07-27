import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(records: list, state: str = "EXECUTED") -> list:
    """
    Фильтрует операции по заданному состоянию.

    :param records: Список операций.
    :param state: Состояние для фильтрации (по умолчанию 'EXECUTED').
    :return: Отфильтрованный список операций.
    """
    return [record for record in records if state == record.get("state")]


def sort_by_date(records: list, ascending: bool = True) -> list:
    """
    Сортирует операции по возрастанию (по умолчанию).

    :param records: Список операций.
    :param ascending: Параметр для сортировки по дате (по умолчанию True - сортировка по возростанию).
    :return: Отсортированный список операций.
    """
    # sort_key = lambda record: datetime.strptime(record['date'], '%Y-%m-%dT%H:%M:%S.%f')
    # flake8:  src/processing.py:20:5: E731 do not assign a lambda expression, use a def

    # Если создавать лямбда-функцию в функции сортировки, то строка получается слишком длинной
    # flake8:  src/processing.py:23:120: E501 line too long (142 > 119 characters)

    def sort_key(record: Dict[str, Any]) -> datetime:
        """
        Используется в качестве ключа сортировки в функции sorted(), извлекая дату из записи.

        :param record: Запись, содержащая дату и время в формате ISO 8601.
        :return: Объект datetime, полученный из строки даты, который используется в качестве ключа сортировки.
        """
        date_str = record.get("date", "")
        date_str = date_str.rstrip("Z")  # Удалить суффикс 'Z', если он присутствует
        formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"]

        for format in formats:
            try:
                return datetime.strptime(date_str, format)
            except ValueError:
                continue
        raise ValueError(f"Date format not recognized: {date_str}")

    return sorted(records, key=sort_key, reverse=not ascending)


def search_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, в описании которых содержится заданная строка поиска.

    :param transactions: Список словарей с данными о банковских операциях.
    :param search_string: Строка поиска, по которой фильтруются транзакции.
    :return: Список транзакций, в описании которых содержится строка поиска.
    """
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [transaction for transaction in transactions if pattern.search(transaction.get("description", ""))]


def count_transactions_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций для каждой категории на основе описаний транзакций.

    :param transactions: Список словарей с данными о банковских операциях.
    :param categories: Список категорий для классификации транзакций.
    :return: Словарь, где ключи — названия категорий, а значения — это количество операций в каждой категории.
    """
    categories_lower = [category.lower() for category in categories]
    categories_used = []
    for transaction in transactions:
        description = transaction.get("description", "").lower()
        for category in categories_lower:
            if category in description:
                categories_used.append(category)
    # Преобразование категорий обратно в исходный регистр и возвращение результата
    return Counter([categories[categories_lower.index(category)] for category in categories_used])
