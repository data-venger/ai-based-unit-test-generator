from my_codes.airflow import airflow_run_addition
from pytest import mark

@mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (4, 5, 9),
])
def test_airflow_run_addition(a, b, expected):
    assert airflow_run_addition(a, b) == expected

def test_airflow_run_addition_negative(monkeypatch):
    # Mock time to return a specific value
    monkeypatch.setattr("time.time", lambda: 12345)

    # Mock random to return a specific value
    monkeypatch.setattr("random.random", lambda: 0.5)

    # Call the function with specific values
    result = airflow_run_addition(10, 20)

    # Assert the result
    assert result == 30
