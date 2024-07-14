from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pytest

from src.external_api import API_KEY, get_transaction_amount_in_rub


def test_get_transaction_amount_in_rub_success(transactions: List[Dict[str, Any]]) -> None:
    """
    Проверяет, что функция get_transaction_amount_in_rub возвращает правильную сумму транзакции в рублях,
    если запрос к API прошел успешно и был получен корректный ответ.

    :param transactions: Список словарей с данными о транзакциях, предоставленный фикстурой.
    :return: None
    """
    transaction = transactions[1]  # USD

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "result": "8740.0"}
        mock_get.return_value = mock_response

        result = get_transaction_amount_in_rub(transaction)

        assert result == 8740.0
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert?from=USD&to=RUB&amount=100.0",
            headers={"apikey": API_KEY},
        )


def test_get_transaction_amount_in_rub_failure(transactions: List[Dict[str, Any]]) -> None:
    """
    Проверяет, что функция get_transaction_amount_in_rub выбрасывает исключение ValueError,
    если запрос к API завершился с ошибкой.

    :param transactions: Список словарей с данными о транзакциях, предоставленный фикстурой.
    :return: None
    """
    transaction = transactions[1]  # USD

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with pytest.raises(ValueError):
            get_transaction_amount_in_rub(transaction)

        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert?from=USD&to=RUB&amount=100.0",
            headers={"apikey": API_KEY},
        )


def test_get_transaction_amount_in_rub_invalid_response(transactions: List[Dict[str, Any]]) -> None:
    """
    Проверяет, что функция get_transaction_amount_in_rub выбрасывает исключение ValueError,
    если ответ от API содержит ошибку.

    :param transactions: Список словарей с данными о транзакциях, предоставленный фикстурой.
    :return: None
    """
    transaction = transactions[1]  # USD

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": False, "error": {"code": 123, "message": "Invalid request"}}
        mock_get.return_value = mock_response

        with pytest.raises(ValueError):
            get_transaction_amount_in_rub(transaction)

        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert?from=USD&to=RUB&amount=100.0",
            headers={"apikey": API_KEY},
        )


def test_get_transaction_amount_in_rub_rub(transactions: List[Dict[str, Any]]) -> None:
    """
    Проверяет, что функция get_transaction_amount_in_rub корректно обрабатывает транзакции в рублях.

    :param transactions: Список словарей с данными о транзакциях, предоставленный фикстурой.
    :return: None
    """
    transaction = transactions[0]  # RUB
    result = get_transaction_amount_in_rub(transaction)
    assert result == 100000.0
