def factors_of_a_number(number):
    """
    Finds all factors of a given number, including negative factors for negative numbers.

    Parameters:
    number (int): The number to find factors for.

    Returns:
    list: A sorted list of all factors of the number.
    """
    if number == 0:
        print("Factors are not defined for zero")

    factors = []

    num = abs(number)

    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)

    if number < 0:
        negative_factors = []
        for f in factors:
            negative_factors.append(-f)

        factors = factors + negative_factors

    factors.sort()

    return factors

def main():
    user_input = input("Enter a number: ")

    try:
        number = int(user_input)
        result = factors_of_a_number(number)
        print("Factors are:", result)
    except:
        print("Invalid input")

if __name__ == "__main__":
    main()