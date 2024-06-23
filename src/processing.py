def filter_by_state(records: list, state: str = "EXECUTED") -> list:
    """
    Принимает на вход список словарей и значение для ключа "state" (опционально) и возвращает новый список,
    содержащий только те словари, у которых ключ "state" содержит переданное в функцию значение

    state: принимает значение "EXECUTED" или "CANCELED", по умолчанию "EXECUTED"
    """
    return [record for record in records if state == record.get("state")]
