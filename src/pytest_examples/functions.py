from math import sqrt


def is_prime(number: int) -> bool:
    """Check if the given number is a prime number.

    Args:
        number: The number to check.

    Returns:
        True if the number is a prime number. False otherwise.
    """
    if not isinstance(number, int):
        raise TypeError("Number must be an integer.")
    if number <= 1:
        return False
    for i in range(2, int(sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True
