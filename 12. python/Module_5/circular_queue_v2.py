class CircularQueue:
    """Represent a circular queue using a fixed-size list."""

    def __init__(self, queue_size):
        """Initialize the circular queue with the given maximum size."""
        self.queue = [None] * queue_size
        self.queue_size = queue_size
        self.front_pos = -1
        self.rear_pos = -1

    def enqueue(self, value):
        """Insert a value at the rear of the circular queue."""
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
        """Remove and display the value at the front of the circular queue."""
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
        """Display the front value of the circular queue."""
        if self.is_empty():
            print("Circular Queue is Empty")
        else:
            print(self.queue[self.front_pos])

    def rear(self):
        """Display the rear value of the circular queue."""
        if self.is_empty():
            print("Circular Queue is Empty")
        else:
            print(self.queue[self.rear_pos])

    def display(self):
        """Display active circular queue elements in logical order."""
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
        """Return True when the circular queue has no elements."""
        return self.front_pos == -1

    def is_full(self):
        """Return True when the circular queue has reached its capacity."""
        return (self.rear_pos + 1) % self.queue_size == self.front_pos


def parse_input_value(raw_value):
    """Convert numeric text to number, otherwise keep as string."""
    try:
        if "." in raw_value:
            return float(raw_value)
        return int(raw_value)
    except ValueError:
        return raw_value


def create_circular_queue():
    """Read circular queue size and create an instance."""
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
    """Handle circular queue menu operations."""
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
                item = parse_input_value(raw_item)
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


def main():
    """Program entry point."""
    circular_queue = create_circular_queue()
    handle_circular_queue_operations(circular_queue)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Unexpected error: {error}")
