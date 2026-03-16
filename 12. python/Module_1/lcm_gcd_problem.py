def gcd(number1, number2) -> int:
    """
    Calculate the Greatest Common Divisor (GCD) of two integers.

    The function finds the largest positive integer that divides both input numbers without leaving a remainder.

    Args:
        number1 (int): First integer.
        number2 (int): Second integer.

    Returns:
        int: The greatest common divisor of number1 and number2.
    """
    gcd_result = 1

    for i in range(1, min(number1, number2) + 1):
        if number1 % i == 0 and number2 % i == 0:
            gcd_result = i

    return gcd_result


def lcm(number1, number2, gcd_value):
    """
    Calculate the Least Common Multiple (LCM) of two integers.

    The function uses the mathematical relationship:
        LCM(a, b) = (a * b) // GCD(a, b)

    Args:
        number1 (int): First integer.
        number2 (int): Second integer.
        gcd_value (int): Precomputed GCD of number1 and number2.

    Returns:
        int: The least common multiple of the two numbers.
    """
    return (number1 * number2) // gcd_value


number1 = int(input("Enter number 1: "))
number2 = int(input("Enter number 2: "))

gcd_result = gcd(number1, number2)

print(gcd_result)
print(lcm(number1, number2, gcd_result))