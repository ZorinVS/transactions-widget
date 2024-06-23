from datetime import datetime


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

    def sort_key(record: dict) -> datetime:
        """Используется в качестве ключа сортировки в функции sorted()"""
        return datetime.strptime(record["date"], "%Y-%m-%dT%H:%M:%S.%f")

    return sorted(records, key=sort_key, reverse=not ascending)
