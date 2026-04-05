class CircularQueue:
    """
        Represents a circular queue data structure.

        Parameters:
        queue_size (int): Maximum number of elements queue can hold.

        Returns:
        None
    """

    def __init__(self, queue_size):
        """
            Initializes a circular queue instance.

            Parameters:
            queue_size (int): Maximum capacity of circular queue.

            Returns:
            None
        """
        self.queue = [None] * queue_size
        self.queue_size = queue_size
        self.front_pos = -1
        self.rear_pos = -1

    def enqueue(self, value):
        """
            Inserts an element at rear of circular queue.

            Parameters:
            value (Any): Value to enqueue.

            Returns:
            None
        """
        if self.is_full():
            print("Circular Queue is Full")
        elif self.is_empty():
            self.front_pos = 0
            self.rear_pos = 0
            self.queue[self.rear_pos] = value
        else:
            self.rear_pos = (self.rear_pos + 1) % self.queue_size
            self.queue[self.rear_pos] = value

    def dequeue(self):
        """
            Removes and returns front element from circular queue.

            Parameters:
            None

            Returns:
            Any | None: Removed front value, or None when queue is empty.
        """
        if self.is_empty():
            print("Circular Queue is Empty")
            return None

        value = self.queue[self.front_pos]
        self.queue[self.front_pos] = None

        if self.front_pos == self.rear_pos:
            self.front_pos = -1
            self.rear_pos = -1
        else:
            self.front_pos = (self.front_pos + 1) % self.queue_size

        print(f"Dequeued: {value}")
        return value

    def front(self):
        """
            Displays front element of circular queue.

            Parameters:
            None

            Returns:
            None
        """
        if self.is_empty():
            print("Circular Queue is Empty")
        else:
            print(self.queue[self.front_pos])

    def rear(self):
        """
            Displays rear element of circular queue.

            Parameters:
            None

            Returns:
            None
        """
        if self.is_empty():
            print("Circular Queue is Empty")
        else:
            print(self.queue[self.rear_pos])

    def display(self):
        """
            Displays active elements in logical circular order.

            Parameters:
            None

            Returns:
            None
        """
        if self.is_empty():
            print("Circular Queue is Empty")
            return

        elements = []
        index = self.front_pos

        while True:
            elements += [self.queue[index]]
            if index == self.rear_pos:
                break
            index = (index + 1) % self.queue_size

        print(elements)

    def is_empty(self):
        """
            Checks whether circular queue is empty.

            Parameters:
            None

            Returns:
            bool: True when empty, else False.
        """
        return self.front_pos == -1

    def is_full(self):
        """
            Checks whether circular queue is full.

            Parameters:
            None

            Returns:
            bool: True when full, else False.
        """
        return (self.rear_pos + 1) % self.queue_size == self.front_pos


def create_circular_queue():
    """
        Reads circular queue size from user and creates object.

        Parameters:
        None

        Returns:
        CircularQueue: Created circular queue instance.
    """
    while True:
        try:
            queue_size = int(input("Enter size of circular queue:- "))
            if queue_size <= 0:
                print("Please Enter Positive Number or Greater than 0")
            else:
                return CircularQueue(queue_size)
        except ValueError:
            print("Please Enter Valid Input")


def handle_circular_queue_operations(circular_queue):
    """
        Handles circular queue menu operations.

        Parameters:
        circular_queue (CircularQueue): Circular queue instance.

        Returns:
        None
    """
    should_continue = True

    while should_continue:
        try:
            print("\n1. Enqueue")
            print("2. Dequeue")
            print("3. Front")
            print("4. Rear")
            print("5. Display")
            print("6. IsEmpty")
            print("7. IsFull")
            print("8. Exit")
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
                circular_queue.enqueue(item)

            elif menu_choice == 2:
                circular_queue.dequeue()

            elif menu_choice == 3:
                circular_queue.front()

            elif menu_choice == 4:
                circular_queue.rear()

            elif menu_choice == 5:
                circular_queue.display()

            elif menu_choice == 6:
                if circular_queue.is_empty():
                    print("Circular Queue is Empty")
                else:
                    print("Circular Queue is Not Empty")

            elif menu_choice == 7:
                if circular_queue.is_full():
                    print("Circular Queue is Full")
                else:
                    print("Circular Queue is Not Full")

            elif menu_choice == 8:
                should_continue = False

            else:
                print("Invalid Choice")

        except ValueError:
            print("Please Enter Valid Input")
        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    circular_queue = create_circular_queue()
    handle_circular_queue_operations(circular_queue)
