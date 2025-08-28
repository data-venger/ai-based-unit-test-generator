import pytest

from my_codes.math_task import run_addition

def test_run_addition_positive():
    result = run_addition(5, 3)
    assert result == 8

def test_run_addition_negative():
    result = run_addition(-2, -3)
    assert result == -5

def test_run_addition_mixed():
    result = run_addition(2, -1)
    assert result == 1

def test_run_addition_zero():
    result = run_addition(0, 0)
    assert result == 0

def test_run_addition_time_patching(monkeypatch):
    def mock_time_now():
        return 1672502400  # Specific timestamp

    monkeypatch.setattr("time.time", mock_time_now)
    result = run_addition(1, 2)
    assert result == 3
