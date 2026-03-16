def selection_sort(list_of_number):
    """
    Sort a list of integers in ascending order using the Selection Sort algorithm.

    Args:
        list_of_number (list[int]): List of integers to be sorted.

    Returns:
        None: The list is sorted in-place.
    """
    for i in range(len(list_of_number)):
        index = i

        for j in range(i+1, len(list_of_number)):

            if list_of_number[j] < list_of_number[index]:
                index = j

        list_of_number[i], list_of_number[index] = list_of_number[index], list_of_number[i]

list_of_number = [5, 3, 4, 2, 1]
selection_sort(list_of_number)

print(list_of_number)