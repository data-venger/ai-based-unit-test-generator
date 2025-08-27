import pytest

from my_codes.math_task import run_addition

def test_run_addition_positive():
    assert run_addition(5, 3) == 8

def test_run_addition_negative():
    assert run_addition(-2, -3) == -5

def test_run_addition_zero():
    assert run_addition(0, 0) == 0

def test_run_addition_float():
    assert run_addition(2.5, 3.5) == 6.0

def test_run_addition_patch_time():
    from datetime import datetime

    def mock_now(cls):
        return datetime(2023, 4, 1, 12, 0, 0)

    with pytest.MonkeyPatch.context() as mp:
        mp.patch('datetime.datetime.now', mock_now)
        assert run_addition(1, 2) == 3

def test_run_addition_patch_random():
    import random

    def mock_random(cls):
        return 0.5

    with pytest.MonkeyPatch.context() as mp:
        mp.patch('random.random', mock_random)
        assert run_addition(1, 2) == 3
