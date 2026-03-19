def create_matrix(matrix_name):
    """Create a 3x3 matrix using user input."""
    matrix = []

    for row in range(3):
        row_list = []
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
                        row_list.append(value)
                        break
                except ValueError:
                    print("Please enter a valid number")
                except Exception as error:
                    print(error)

        matrix.append(row_list)

    return matrix


def determinant(matrix):
    """Return the determinant of a 3x3 matrix."""

    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[0][2]

    d = matrix[1][0]
    e = matrix[1][1]
    f = matrix[1][2]

    g = matrix[2][0]
    h = matrix[2][1]
    i = matrix[2][2]

    det = (a * (e*i - f*h)) - (b * (d*i - f*g)) + (c * (d*h - e*g))

    return det


if __name__ == "__main__":
    matrix_1 = create_matrix("matrix")

    try:
        print(determinant(matrix_1))
    except ValueError:
        print("Please enter a valid number")
    except IndexError:
        print("Index out of range")
    except Exception as error:
        print(error)
