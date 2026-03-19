
class CircularQueue:

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
        else:
            value = self.queue[self.front_pos]
            self.queue[self.front_pos] = None

            if self.front_pos == self.rear_pos:
                self.front_pos = -1
                self.rear_pos = -1
            else:
                self.front_pos = (self.front_pos + 1) % self.queue_size

            print(f"Dequeued: {value}")

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
        """Display the actual internal array of the circular queue."""
        if self.is_empty():
            print("Circular Queue is Empty")
        else:
            print(self.queue)

    def is_empty(self):
        """Return True when the circular queue has no elements."""
        return self.front_pos == -1

    def is_full(self):
        """Return True when the circular queue has reached its capacity."""
        return (self.rear_pos + 1) % self.queue_size == self.front_pos


while True:
    try:
        queue_size = int(input("Enter size of circular queue:- "))
        if queue_size <= 0:
            print("Please Enter Positive Number or Greater than 0")
        else:
            circular_queue = CircularQueue(queue_size)
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
        print("3. Front")
        print("4. Rear")
        print("5. Display")
        print("6. IsEmpty")
        print("7. IsFull")
        print("8. Exit")
        print()

        menu_choice = int(input("Enter your choice:- "))

        if menu_choice == 1:
            item = int(input("Enter Number to Enqueue:- "))
            if item <= 0:
                print("Please Enter Positive Number or Greater than 0")
            else:
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
            should_exit = False

        else:
            print("Invalid Choice")

    except ValueError:
        print("Please Enter Valid Input")
    except Exception as error:
        print(error)
