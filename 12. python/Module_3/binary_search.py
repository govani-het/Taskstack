from insertion_sort import insertion_sorts



def binary_search(list_of_number, number):
    """
    Perform binary search on a sorted list to find a target number.

    Args:
        list_of_number (list[int]): A sorted list of integers where the
            search operation will be performed.
        number (int): The target value to search for in the list.

    Returns:
        None: Prints the index of the element if found, otherwise
        prints that the element was not found.
    """
    start = 0
    end = len(list_of_number) - 1
    while start <= end:
        mid = (start + end) // 2
        if list_of_number[mid] == number:
            print("Element is present at index " + str(mid))
            return
        elif list_of_number[mid] < number:
            start = mid + 1
        else:
            end = mid - 1
    print("Element not found")


list_of_number = [23,45,67,334,56]
sorted_list = insertion_sorts(list_of_number)
print(sorted_list)
number = int(input("Enter the number: "))
binary_search(sorted_list, number)