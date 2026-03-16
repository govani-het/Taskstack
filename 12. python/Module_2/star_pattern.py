def star_pattern(original_number):
    for row in range(original_number):
        for col in range(row + 1):
            print("*", end=" ")
        print()

number = int(input("Enter a number: "))
star_pattern(number)