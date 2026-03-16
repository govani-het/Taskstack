def factors_of_a_number(number):
    """
    Return all factors of a given integer.

    Args:
        number (int): The integer for which factors need to be calculated.

    Returns:
        list[int]: A list containing all factors of the given number
        from 1 up to the number itself.
    """
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

number = int(input("Enter a number: "))
print(factors_of_a_number(number))