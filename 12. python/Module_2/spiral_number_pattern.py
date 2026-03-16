def spiral_number_pattern(number):
    count = 1
    top = 0
    bottom = number - 1
    left = 0
    right = number - 1

    matrix = []

    for i in range(number):
        row = []
        for j in range(number):
            row.append(0)
        matrix.append(row)

    while top <= bottom and left <= right:

        # left to right
        for i in range(left,right+1):
            matrix[top][i] = count
            count += 1
        top += 1

        # top to bottom
        for i in range(top,bottom+1):
            matrix[i][right] = count
            count += 1
        right -= 1

        # right to left
        for i in range(right,left-1,-1):
            matrix[bottom][i] = count
            count += 1
        bottom -= 1

        # bottom to up
        for i in range(bottom,top-1,-1):
            matrix[i][left] = count
            count += 1
        left += 1

    return matrix

number = int(input("Enter a number: "))
result = spiral_number_pattern(number)

for i in result:
    for j in i:
        print(j, end=" ")
    print()