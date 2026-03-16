def number_pattern(original_number):
    for row in range(original_number, 0, -1):
        for col in range(row):
            print(col + 1, end=" ")
        print()

number = int(input("Enter a number: "))
number_pattern(number)