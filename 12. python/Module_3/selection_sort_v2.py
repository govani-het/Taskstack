def selection_sort(numbers):
    """
    Sort a list of numbers using Selection Sort.

    Avoids unnecessary swapping when element is already in correct position.

    Args:
        numbers (list): List of numbers.

    Returns:
        None: Sorts the list in-place.
    """

    n = len(numbers)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            if numbers[j] < numbers[min_index]:
                min_index = j

        if min_index != i:
            numbers[i], numbers[min_index] = numbers[min_index], numbers[i]


numbers = [5, 3, 4, 2, 1]
selection_sort(numbers)
print(numbers)