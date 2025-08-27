import pytest
from my_codes.math_task import add_numbers

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-5, 10, 5),
    (0, 0, 0),
])
def test_add_numbers(a, b, expected):
    assert add_numbers(a, b) == expected

def test_add_numbers_with_negative(monkeypatch):
    def mock_add_numbers(a, b):
        return -1
    monkeypatch.setattr(my_codes.math_task, "add_numbers", mock_add_numbers)
    assert add_numbers(1, 2) == -1
