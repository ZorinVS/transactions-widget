from typing import Iterator


def filter_by_currency(transactions: list[dict], code: str) -> Iterator[dict]:
    """
    Возвращает итератор, который выдает по очереди операции, в которых указана заданная валюта.

    :param transactions: Список операций.
    :param code: Код валюты.
    :return: Итератор, выдающий по очереди операции, в которых указана заданная валюта.
    """
    return (transaction for transaction in transactions if transaction["operationAmount"]["currency"]["code"] == code)


def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """
    Генератор, возвращающий описание каждой операции по очереди.

    :param transactions: Список операций.
    :return: Генератор, который поочередно возвращает описания операций из каждого словаря в списке transactions.
    """
    return (transaction["description"] for transaction in transactions)


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Возвращает по очереди номера карт в формате XXXX XXXX XXXX XXXX, где X — цифра.

    :param start: Начало диапазона генерации.
    :param end: Конец диапазона генерации (включительно).
    :return: Генератор, который поочередно возвращает номера карт.
    """
    for num in range(start, end+1):
        # Получение номера карты в виде слитной строки
        formatted_num = f"{num:016d}"
        # Вывод номера карты в формате XXXX XXXX XXXX XXXX
        yield f"{formatted_num[:4]} {formatted_num[4:8]} {formatted_num[8:12]} {formatted_num[12:]}"
