import math


def sum_numbers(a: float, b: float) -> float:
    """
    Sum two numbers and return the result.
    
    Args:
        a (float): First number to add
        b (float): Second number to add
        
    Returns:
        float: The sum of a and b
    """
    return a + b


def multiply_numbers(a: float, b: float) -> float:
    """
    Multiply two numbers and return the result.
    
    Args:
        a (float): First number to multiply
        b (float): Second number to multiply
        
    Returns:
        float: The product of a and b
    """
    return a * b


def subtract_numbers(a: float, b: float) -> float:
    """
    Subtract the second number from the first and return the result.
    
    Args:
        a (float): Number to subtract from
        b (float): Number to subtract
        
    Returns:
        float: The difference of a and b
    """
    return a - b


def divide_numbers(a: float, b: float) -> float:
    """
    Divide the first number by the second and return the result.
    
    Args:
        a (float): Number to divide (dividend)
        b (float): Number to divide by (divisor)
        
    Returns:
        float: The quotient of a and b
        
    Raises:
        ValueError: If b is zero (division by zero)
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: float, exponent: float) -> float:
    """
    Raise the base to the power of the exponent.
    
    Args:
        base (float): The base number
        exponent (float): The exponent
        
    Returns:
        float: The result of base raised to the power of exponent
    """
    return base ** exponent


def square_root(number: float) -> float:
    """
    Calculate the square root of a number.
    
    Args:
        number (float): The number to find the square root of
        
    Returns:
        float: The square root of the number
        
    Raises:
        ValueError: If number is negative
    """
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(number)