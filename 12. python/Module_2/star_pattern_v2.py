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
        print("* " * (row + 1))

while True:
    try:
        user_input = int(input("Enter a number: "))
        
        if user_input <= 0:
            print("Number must be positive (greater than 0).")
            continue

        break
        
    except ValueError:
        print("Invalid input. Please enter a valid integer.")


star_pattern(user_input)