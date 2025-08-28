def add_numbers(a: int, b: int) -> int:
    """Simple function to add two numbers."""
    return a + b


def run_addition(a: int, b: int) -> int:
    """Wrapper to add numbers and print result."""
    result = add_numbers(int(a), int(b))
    print(f"Result of {a} + {b} = {result}")
    return result
