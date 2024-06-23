from datetime import datetime


def filter_by_state(records: list, state: str = "EXECUTED") -> list:
    """
    Принимает на вход список словарей и значение для ключа "state" (опционально) и возвращает новый список,
    содержащий только те словари, у которых ключ "state" содержит переданное в функцию значение

    state: принимает значение "EXECUTED" или "CANCELED", по умолчанию "EXECUTED"
    """
    return [record for record in records if state == record.get("state")]


def sort_by_date(records: list, sort_by_date: str = "descending") -> list:
    """
    Принимает на вход список словарей и значение параметра сортировки (опционально) и возвращает отсортированный список

    sort_by_date: принимает значение "descending" или "ascending", по умолчанию "descending"
    """
    # sort_key = lambda record: datetime.strptime(record['date'], '%Y-%m-%dT%H:%M:%S.%f')
    # flake8:  src/processing.py:20:5: E731 do not assign a lambda expression, use a def

    # Если создавать лямбда-функцию в функции сортировки, то строка получается слишком длинной
    # flake8:  src/processing.py:23:120: E501 line too long (142 > 119 characters)

    def sort_key(record: dict) -> datetime:
        """Используется в качестве ключа сортировки в функции sorted()"""
        return datetime.strptime(record["date"], "%Y-%m-%dT%H:%M:%S.%f")

    return sorted(records, key=sort_key, reverse=sort_by_date == "descending")
