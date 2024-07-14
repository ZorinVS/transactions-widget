import json
import os
from typing import Any, Dict, List


def read_transactions_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Возвращает список словарей с данными о финансовых транзакциях.

    :param file_path: Путь к json-файлу.
    :return: Список транзакций.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path) as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []

    except (json.JSONDecodeError, IOError):
        return []
