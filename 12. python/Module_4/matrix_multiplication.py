def create_matrix(matrix_name):
    """Create a 3x3 matrix using user input."""
    matrix = []

    for row in range(3):
        row_data = []
        for col in range(3):
            while True:
                try:
                    value = int(
                        input(
                            f"Enter value for {matrix_name} at position "
                            f"[{row}][{col}]: "
                        )
                    )
                    if value < 0:
                        print("Negative numbers are not allowed")
                    else:
                        row_data.append(value)
                        break
                except ValueError:
                    print("Please enter a valid number")
                except Exception as error:
                    print(error)

        matrix.append(row_data)

    return matrix


def matrix_multiplication(matrix_1, matrix_2):
    """Return the multiplication of two 3x3 matrices."""
    result_matrix = []

    for row in range(3):
        row_data = []
        for col in range(3):
            value = 0
            for index in range(3):
                value += matrix_1[row][index] * matrix_2[index][col]
            row_data.append(value)
        result_matrix.append(row_data)

    return result_matrix
if __name__ == "__main__":
    matrix_1 = create_matrix("matrix 1")
    matrix_2 = create_matrix("matrix 2")

    print(matrix_multiplication(matrix_1, matrix_2))
