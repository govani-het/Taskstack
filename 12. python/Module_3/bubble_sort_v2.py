def bubble_sort(numbers):
    """
    Sort a list of numbers in ascending order using Bubble Sort.

    This version uses a flag to stop early if the list is already sorted.

    Args:
        numbers (list[int]): List of integers to sort.

    Returns:
        None: Sorts the list in-place.
    """
    n = len(numbers)

    for i in range(n - 1):
        swapped = False

        for j in range(n - 1 - i):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                swapped = True

        if not swapped:
            break


numbers = [5, 3, 8, 4, 2]
bubble_sort(numbers)
print(numbers)