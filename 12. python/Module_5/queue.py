
class Queue:
    """Represent a basic queue using a Python list."""

    def __init__(self, queue_size):
        """Initialize the queue with the given maximum size."""
        self.items = []
        self.front_index = -1
        self.rear_index = -1
        self.capacity = queue_size

    def enqueue(self, item):
        """Insert a value at the rear of the queue."""

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
        """Return True when the queue has no active elements."""
        return self.front_index == -1

    def dequeue(self):
        """Remove the value at the front of the queue."""
        if self.is_empty():
            print("Queue is empty")
            return

        print(f"{self.items[self.front_index]} removed")

        self.front_index += 1

        if self.front_index > self.rear_index:
            self.front_index = -1
            self.rear_index = -1
            self.items = []

    def peek(self):
        """Display the value at the front of the queue."""

        if self.is_empty():
            print("Queue is empty")

        else:
            print(self.items[self.front_index])

    def display_queue(self):
        """Display the current queue contents."""
        if self.is_empty():
            print("Queue is empty")
        else:
            print(self.items[self.front_index:self.rear_index+1])



    def is_full(self):
        """Return True when the queue has reached its maximum size."""

        if self.rear_index == self.capacity - 1:
            return True

        return False

while True:
    try:
        queue_size = int(input("Enter size of queue:- "))
        if queue_size <= 0:
            print("Please Enter Positive Number or Greater than 0")
        else:
            queue = Queue(queue_size)
            break
    except ValueError:
        print("Please Enter Valid Input")
    except Exception as error:
        print(error)


should_exit = True

while should_exit:
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
            item = int(input("Enter Number to Enqueue:- "))
            if item <= 0:
                print("Please Enter Positive Number or Greater than 0")
            else:
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
            should_exit = False

        else:
            print("Invalid Choice")

    except ValueError:
        print("Please Enter Valid Input")
    except Exception as error:
        print(error)
