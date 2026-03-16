def gcd(number1, number2) -> int:
    """Return the greatest common divisor of two numbers."""
    gcd_result = 1

    for i in range(1, min(number1, number2) + 1):
        if number1 % i == 0 and number2 % i == 0:
            gcd_result = i

    return gcd_result


def lcm(number1, number2, gcd_value):
    """Return the least common multiple of two numbers."""
    return (number1 * number2) // gcd_value


number1 = int(input("Enter number 1: "))
number2 = int(input("Enter number 2: "))

gcd_result = gcd(number1, number2)

print(gcd_result)
print(lcm(number1, number2, gcd_result))