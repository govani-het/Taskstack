def incremental_number_pattern(number):
    count = 1
    for row in range(number):
        for column in range(row + 1):
            print(count, end=" ")
            count += 1
        print()


number = int(input("Enter a number: "))
incremental_number_pattern(number)