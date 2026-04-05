class Queue:
    """
        Represents a linear queue data structure.

        Parameters:
        queue_size (int): Maximum number of elements queue can hold.

        Returns:
        None
    """

    def __init__(self, queue_size):
        """
            Initializes a queue instance.

            Parameters:
            queue_size (int): Maximum capacity of queue.

            Returns:
            None
        """
        self.items = []
        self.front_index = -1
        self.rear_index = -1
        self.capacity = queue_size

    def enqueue(self, item):
        """
            Inserts an element at the rear of queue.

            Parameters:
            item (Any): Value to enqueue.

            Returns:
            None
        """
        if self.is_full():
            print("Queue is full")
        else:
            if self.front_index == -1:
                self.rear_index = 0
                self.front_index = 0
                self.items += [item]
            else:
                self.items += [item]
                self.rear_index += 1

    def is_empty(self):
        """
            Checks whether queue has active elements.

            Parameters:
            None

            Returns:
            bool: True when empty, else False.
        """
        if self.front_index == -1:
            return True
        return self.front_index > self.rear_index

    def dequeue(self):
        """
            Removes and returns front element from queue.

            Parameters:
            None

            Returns:
            Any | None: Removed front element, or None when queue is empty.
        """
        if self.is_empty():
            print("Queue is empty")
            return None

        dequeued_value = self.items[self.front_index]
        self.front_index += 1

        print(f"Dequeued: {dequeued_value}")
        return dequeued_value

    def peek(self):
        """
            Displays current front element.

            Parameters:
            None

            Returns:
            None
        """
        if self.is_empty():
            print("Queue is empty")
        else:
            print(self.items[self.front_index])

    def display_queue(self):
        """
            Displays all active queue elements.

            Parameters:
            None

            Returns:
            None
        """
        if self.is_empty():
            print("Queue is empty")
        else:
            print(self.items[self.front_index:self.rear_index + 1])

    def is_full(self):
        """
            Checks whether queue reached capacity.

            Parameters:
            None

            Returns:
            bool: True when full, else False.
        """
        return self.rear_index == self.capacity - 1


def create_queue():
    """
        Reads queue size from user and creates queue object.

        Parameters:
        None

        Returns:
        Queue: Created queue instance.
    """
    while True:
        try:
            queue_size = int(input("Enter size of queue:- "))
            if queue_size <= 0:
                print("Please Enter Positive Number or Greater than 0")
            else:
                return Queue(queue_size)
        except ValueError:
            print("Please Enter Valid Input")


def handle_queue_operations(queue):
    """
        Handles queue menu operations.

        Parameters:
        queue (Queue): Queue instance used for operations.

        Returns:
        None
    """
    should_continue = True

    while should_continue:
        try:
            print("\n1. Enqueue")
            print("2. Dequeue")
            print("3. Peek")
            print("4. Display")
            print("5. IsEmpty")
            print("6. Exit")
            print()

            menu_choice = int(input("Enter your choice:- "))

            if menu_choice == 1:
                raw_item = input("Enter value to Enqueue:- ")
                try:
                    if "." in raw_item:
                        item = float(raw_item)
                    else:
                        item = int(raw_item)
                except ValueError:
                    item = raw_item
                queue.enqueue(item)

            elif menu_choice == 2:
                queue.dequeue()

            elif menu_choice == 3:
                queue.peek()

            elif menu_choice == 4:
                queue.display_queue()

            elif menu_choice == 5:
                if queue.is_empty():
                    print("Queue is Empty")
                else:
                    print("Queue is Not Empty")

            elif menu_choice == 6:
                should_continue = False

            else:
                print("Invalid Choice")

        except ValueError:
            print("Please Enter Valid Input")
        except Exception as error:
            print(f"Error: {error}")



if __name__ == "__main__":
    queue = create_queue()
    handle_queue_operations(queue)
