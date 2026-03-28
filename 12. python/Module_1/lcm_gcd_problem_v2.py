def gcd(number1, number2):
    """
    Calculate the Greatest Common Divisor (GCD) of two integers.
    
    Handles negative numbers by converting to absolute values.
    In real-world scenarios, GCD is calculated using positive values.

    The function finds the largest positive integer that divides both input numbers without leaving a remainder.

    Args:
        number1 (int): First integer.
        number2 (int): Second integer.

    Returns:
        int: The greatest common divisor of number1 and number2.
        
    Raises:
        ValueError: If either number is zero.
    """

    number1 = abs(number1)
    number2 = abs(number2)
    

    if number1 == 0 or number2 == 0:
        raise ValueError("GCD is not defined for zero. Both numbers must be non-zero.")
    
    gcd_result = 1

    for i in range(1, min(number1, number2) + 1):
        if number1 % i == 0 and number2 % i == 0:
            gcd_result = i

    return gcd_result


def lcm(number1, number2, gcd_value):
    """
    Calculate the Least Common Multiple (LCM) of two integers.
    
    Handles negative numbers by converting to absolute values.
    In real-world scenarios, LCM is calculated using positive values.

    The function uses the mathematical relationship:
        LCM(a, b) = (a * b) // GCD(a, b)

    Args:
        number1 (int): First integer.
        number2 (int): Second integer.
        gcd_value (int): Precomputed GCD of number1 and number2.

    Returns:
        int: The least common multiple of the two numbers.
    """

    number1 = abs(number1)
    number2 = abs(number2)
    
    return (number1 * number2) // gcd_value


def get_valid_integer(prompt):
    """
    Get a valid integer input from user with validation.
    Rejects alphabets and special characters.
    
    Args:
        prompt (str): The prompt to display to the user.
        
    Returns:
        int: A valid integer entered by the user.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input:
                print("Error: Input cannot be empty. Please enter a number.")
                continue
            
            if not user_input.lstrip('-').isdigit():
                print(f"Error: '{user_input}' is invalid. Only integers are allowed (no alphabets or special characters).")
                continue
            
            number = int(user_input)
            return number
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    try:

        number1 = get_valid_integer("Enter number 1: ")
        number2 = get_valid_integer("Enter number 2: ")
        
        gcd_result = gcd(number1, number2)
        
        lcm_result = lcm(number1, number2, gcd_result)
    

        print(f"GCD({number1}, {number2}) = {gcd_result}")
        print(f"LCM({number1}, {number2}) = {lcm_result}")
        
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")