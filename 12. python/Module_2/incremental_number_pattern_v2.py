def incremental_number_pattern(number: int) -> None:
    """
    Print a triangular incremental number pattern using a single loop.

    Each row contains consecutive integers, continuing from the previous row.

    Example:
        Input: 5

        Output:
            1
            2 3
            4 5 6
            7 8 9 10
            11 12 13 14 15

    Args:
        number (int): The total number of rows in the pattern.

    Returns:
        None: The function prints the pattern directly to the console.
    """
    count = 1

    for row in range(1, number + 1):
        print(*range(count, count + row))

        count += row


if __name__ == "__main__":
    while True:
        try:
            user_input = int(input("Enter a number: "))

            if user_input <= 0:
                print("Number must be positive, greater than 0.")
                continue

            break

        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    incremental_number_pattern(user_input)