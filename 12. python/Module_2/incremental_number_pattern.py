def incremental_number_pattern(number):
    """
    The function prints numbers sequentially starting from 1 and arranges them in a triangular pattern based on the given number of rows.

    Example (number = 5):
        1
        2 3
        4 5 6
        7 8 9 10
        11 12 13 14 15

    Args:
        number (int): The number of rows to print in the triangle.
    """
    count = 1
    for row in range(number):
        for column in range(row + 1):
            print(count, end=" ")
            count += 1
        print()


number = int(input("Enter a number: "))
incremental_number_pattern(number)