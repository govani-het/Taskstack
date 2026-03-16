def bubble_sort(list_of_number):
    """
    Sort a list of numbers in ascending order using the Bubble Sort algorithm.

    Args:
        list_of_number (list[int]): The list of integers to be sorted.

    Returns:
        None: The function sorts the list in-place and does not return a new list.
    """
    for i in range(len(list_of_number) - 1):

        for j in range(len(list_of_number) - 1 - i):

            if list_of_number[j] > list_of_number[j + 1]:

                list_of_number[j], list_of_number[j + 1] = list_of_number[j + 1], list_of_number[j]


list_of_number = [5, 3, 8, 4, 2]
bubble_sort(list_of_number)
print(list_of_number)