import math

def find_gcd(a, b):
    """Find the greatest common divisor of two numbers."""
    return math.gcd(a, b)  


def count_vowels(s):
    """Count the number of vowels in a string."""
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)
  

def sort_list(lst):
    """Sort a list in ascending order."""
    return sorted(lst)
  
