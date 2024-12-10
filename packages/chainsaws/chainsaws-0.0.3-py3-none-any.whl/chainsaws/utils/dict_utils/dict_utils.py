"""Dictionary utility functions."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterator

T = TypeVar("T")


def divide_chunks(
    data: list[T] | dict[str, T],
    chunk_size: int,
) -> Iterator[list[T] | dict[str, T]]:
    """Split a list or dictionary into chunks of specified size.

    Args:
        data: Input list or dictionary to be chunked
        chunk_size: Size of each chunk

    Returns:
        Iterator yielding chunks of the input data

    Raises:
        ValueError: If chunk_size is less than 1

    Examples:
        >>> list(divide_chunks([1, 2, 3, 4, 5], 2))
        [[1, 2], [3, 4], [5]]

        >>> list(divide_chunks({'a': 1, 'b': 2, 'c': 3}, 2))
        [{'a': 1, 'b': 2}, {'c': 3}]

    """
    if chunk_size < 1:
        msg = "Chunk size must be at least 1"

        raise ValueError(msg)

    if isinstance(data, list):
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]

    elif isinstance(data, dict):
        items = list(data.items())
        for i in range(0, len(items), chunk_size):
            yield dict(items[i:i + chunk_size])


def convert_number_to_decimal(dict_detail: dict) -> dict:
    """Convert all float values in a nested dictionary to Decimal.

    Args:
        dict_detail: Dictionary containing float values to be converted

    Returns:
        dict: The input dictionary with float values converted to Decimal

    """
    for key, value in dict_detail.items():
        if isinstance(value, float):
            dict_detail[key] = Decimal(str(value))
        elif isinstance(dict_detail[key], dict):
            convert_number_to_decimal(dict_detail[key])
        elif isinstance(dict_detail[key], list):
            for item in dict_detail[key]:
                if isinstance(item, dict):
                    convert_number_to_decimal(item)
    return dict_detail


def convert_decimal_to_number(dict_detail: dict) -> dict:
    """Convert all Decimal values in a nested dictionary to int or float.

    Args:
        dict_detail: Dictionary containing Decimal values to be converted

    Returns:
        dict: The input dictionary with Decimal values converted to int/float

    """
    for key, value in dict_detail.items():
        if isinstance(value, Decimal):
            if value % 1 == 0:
                dict_detail[key] = int(value)
            else:
                dict_detail[key] = float(value)
        elif isinstance(dict_detail[key], dict):
            convert_decimal_to_number(dict_detail[key])
        elif isinstance(dict_detail[key], list):
            for item in dict_detail[key]:
                if isinstance(item, dict):
                    convert_decimal_to_number(item)
    return dict_detail
