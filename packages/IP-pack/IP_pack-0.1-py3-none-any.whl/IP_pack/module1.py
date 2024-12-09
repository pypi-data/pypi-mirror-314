def is_palindrome(s):
    """Check if a string is a palindrome."""
    return s == s[::-1]


def fibonacci_series(n):
    """Generate the n-th Fibonacci number using recursion."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_series(n - 1) + fibonacci_series(n - 2)


def factorial(n):
    """Calculate the factorial of n using iteration."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

