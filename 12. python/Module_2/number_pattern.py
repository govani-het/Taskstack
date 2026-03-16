def number_pattern(original_number):
    """
    The function prints numbers starting from 1 up to the row length,while the number of elements decreases by one in each subsequent row.

    Example (original_number = 5):
        1 2 3 4 5
        1 2 3 4
        1 2 3
        1 2
        1

    Args:
        original_number (int): The number of elements in the first row
            and the total number of rows in the pattern.

    Returns:
        None: The function prints the pattern directly to the console.
    """

    for row in range(original_number, 0, -1):
        for col in range(row):
            print(col + 1, end=" ")
        print()

number = int(input("Enter a number: "))
number_pattern(number)