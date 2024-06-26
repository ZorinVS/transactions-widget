from typing import Iterator


def filter_by_currency(transactions: list[dict], code: str) -> Iterator[dict]:
    """
    Возвращает итератор, который выдает по очереди операции, в которых указана заданная валюта.

    :param transactions: Список операций.
    :param code: Код валюты.
    :return: Итератор, выдающий по очереди операции, в которых указана заданная валюта.
    """
    return (transaction for transaction in transactions if transaction["operationAmount"]["currency"]["code"] == code)
