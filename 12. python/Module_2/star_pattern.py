def star_pattern(original_number):
    """
    The function prints a triangle where the number of stars increases by one in each row.

    Example (original_number = 5):
        *
        * *
        * * *
        * * * *
        * * * * *

    Args:
        original_number (int): The total number of rows to print.

    Returns:
        None: The pattern is printed directly to the console.
    """
    for row in range(original_number):
        for col in range(row + 1):
            print("*", end=" ")
        print()

number = int(input("Enter a number: "))
star_pattern(number)