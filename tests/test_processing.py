import pytest
from collections import Counter
from typing import List, Dict, Any

from src.processing import filter_by_state, sort_by_date, search_transactions, count_transactions_by_category


@pytest.mark.parametrize("records, state, expected", [
    (
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}],
        'EXECUTED',
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
    ),
    (
        [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}],
        'CANCELED',
        [{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    )
])
def test_filter_by_state(records, state, expected):
    assert filter_by_state(records, state) == expected


def test_sort_by_date_ascending(records_ascending):
    assert sort_by_date([
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]) == records_ascending


def test_test_sort_by_date_descending(records_descending):
    assert sort_by_date([
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ], False) == records_descending


def test_search_transactions(transactions: List[Dict[str, Any]]) -> None:
    """
    Тестирует поиск по описанию.

    :param transactions: Список словарей с данными о банковских операциях, предоставленный фикстурой.
    :return: None.
    """
    result = search_transactions(transactions, "Перевод организации")
    assert len(result) == 2
    assert result[0]["id"] == 441945886
    assert result[1]["id"] == 41428829


def test_search_transactions_by_piece(transactions: List[Dict[str, Any]]) -> None:
    """
    Тестирует поиск по части слова.

    :param transactions: Список словарей с данными о банковских операциях, предоставленный фикстурой.
    :return: None.
    """
    result = search_transactions(transactions, "вкл")
    assert len(result) == 1
    assert result[0]["id"] == 587085106


def test_search_transactions_no_result(transactions: List[Dict[str, Any]]) -> None:
    """
    Тестирует поиск без нахождения транзакций.

    :param transactions: Список словарей с данными о банковских операциях, предоставленный фикстурой.
    :return: None.
    """
    result = search_transactions(transactions, "покупка")
    assert len(result) == 0


def test_search_transactions_ignorecase(transactions: List[Dict[str, Any]]) -> None:
    """
    Тестирует поиск без учета регистра.

    :param transactions: Список словарей с данными о банковских операциях, предоставленный фикстурой.
    :return: None.
    """
    result = search_transactions(transactions, "СчЕт")
    assert len(result) == 1
    assert result[0]["id"] == 142264268


def test_count_transactions_by_category(transactions: List[Dict[str, Any]], categories: list) -> None:
    """
    Тестирует подсчет транзакций по категориям.

    :param transactions: Список словарей с данными о банковских операциях, предоставленный фикстурой.
    :param categories: Список категорий транзакций, предоставленный фикстурой.
    :return: None.
    """
    result = count_transactions_by_category(transactions, categories)
    expected = Counter({'Перевод': 3, 'Организации': 2, 'Вклад': 1})
    assert result == expected


def test_count_transactions_by_category_non_existent(transactions: List[Dict[str, Any]]) -> None:
    """
    Тестирует подсчет транзакций по категориям, не содержащимся в описании транзакций.

    :param transactions: Список словарей с данными о банковских операциях, предоставленный фикстурой.
    :return: None.
    """
    result = count_transactions_by_category(transactions, ["Недвижимость", "Инвестиции"])
    assert result == Counter()


def test_count_transactions_by_category_without_transactions(categories: list) -> None:
    """
    Тестируем случай, когда нет транзакций.

    :param categories: Список категорий транзакций, предоставленный фикстурой.
    :return: None
    """
    result = count_transactions_by_category([], categories)
    assert result == Counter()


def test_count_transactions_by_category_without_categories(transactions: List[Dict[str, Any]]) -> None:
    """
    Тестируем случай, когда нет категорий.

    :param transactions: Список словарей с данными о банковских операциях, предоставленный фикстурой.
    :return: None
    """
    result = count_transactions_by_category(transactions, [])
    assert result == Counter()
