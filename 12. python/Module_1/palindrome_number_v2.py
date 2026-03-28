def is_palindrome(number):
    """
    Check whether a given number is a palindrome.A palindrome number reads the same forward and backward.

    Args:
        number (int): The number to check.

    Returns:
        bool: True if the number is a palindrome, otherwise False.
    """

    if number < 0:
        return False

    original_number = number
    reversed_number = 0

    while number > 0:
        digit = number % 10
        reversed_number = reversed_number * 10 + digit
        number = number // 10

    return original_number == reversed_number


while True:
    try:
        num = int(input("Enter a number: "))
        break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if is_palindrome(num):
    print(f"{num} is a palindrome.")
else:
    print(f"{num} is not a palindrome.")