def number_pattern(original_number: int) -> None:
    """
    Prints a decreasing number pattern.

    Example (original_number = 5):
        1 2 3 4 5
        1 2 3 4
        1 2 3
        1 2
        1
    """
    for row in range(original_number, 0, -1):
        print(*range(1, row + 1))


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

    number_pattern(user_input)