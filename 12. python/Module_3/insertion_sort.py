def insertion_sorts(list_of_number):

    """
    Sort a list of integers in ascending order using the Insertion Sort algorithm.

    Args:
        list_of_number (list[int]): List of integers to be sorted.

    Returns:
        list[int]: The sorted list in ascending order.
    """

    for i in range(1, len(list_of_number)):
        value = list_of_number[i]
        j = i - 1
        while j >= 0 and list_of_number[j] > value:
            list_of_number[j + 1] = list_of_number[j]
            j -= 1
        list_of_number[j + 1] = value
    return list_of_number

if __name__ == '__main__':
    list_of_number = [5, 4, 3, 2, 1]
    sorted_list = insertion_sorts(list_of_number)
    print(sorted_list)
