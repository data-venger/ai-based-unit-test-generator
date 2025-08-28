import pytest

from my_codes.math_task import add_numbers


def test_add_numbers_positive():
    assert add_numbers(2, 3) == 5


def test_add_numbers_negative():
    assert add_numbers(-2, -3) == -5


def test_add_numbers_zero():
    assert add_numbers(0, 0) == 0


def test_add_numbers_float():
    assert add_numbers(1.5, 2.5) == 4.0


def test_add_numbers_long():
    assert add_numbers(10**9, 10**9) == 2 * 10**9
