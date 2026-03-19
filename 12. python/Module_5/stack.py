
class Stack:
    """Represent a basic stack using a Python list."""

    def __init__(self, capacity):
        """Initialize the stack with the given maximum size."""
        self.items = []
        self.capacity = capacity

    def push(self, item):
        """Insert a value at the top of the stack."""
        if self.is_full():
            print("Stack is Full")
        else:
            self.items += [item]

    def pop(self):
        """Remove the top value from the stack."""
        if self.is_empty():
            print("Stack is Empty")
        else:
            del self.items[-1]
            print("Popped:")

    def peek(self):
        """Display the value at the top of the stack."""
        if self.is_empty():
            print("Stack is Empty")
        else:
            print(self.items[-1])

    def display(self):
        """Display the current stack contents."""
        if self.is_empty():
            print("Stack is Empty")
        else:
            print(self.items)

    def is_empty(self):
        """Return True when the stack has no elements."""
        return len(self.items) == 0

    def is_full(self):
        """Return True when the stack has reached its maximum size."""
        return len(self.items) == self.capacity


while True:
    try:
        stack_size = int(input("Enter size of stack:- "))
        if stack_size <= 0:
            print("Please Enter Positive Number or Greater than 0")
        else:
            stack = Stack(stack_size)
            break
    except ValueError:
        print("Please Enter Valid Input")
    except Exception as error:
        print(error)


should_exit = True

while should_exit:
    try:
        print("\n1. Push")
        print("2. Pop")
        print("3. Peek")
        print("4. Display")
        print("5. IsEmpty")
        print("6. Exit")
        print()

        menu_choice = int(input("Enter your choice:- "))

        if menu_choice == 1:
            item = int(input("Enter Number to Push:- "))
            if item <= 0:
                print("Please Enter Positive Number or Greater than 0")
            else:
                stack.push(item)

        elif menu_choice == 2:
            stack.pop()

        elif menu_choice == 3:
            stack.peek()

        elif menu_choice == 4:
            stack.display()

        elif menu_choice == 5:
            if stack.is_empty():
                print("Stack is Empty")
            else:
                print("Stack is Not Empty")

        elif menu_choice == 6:
            should_exit = False

        else:
            print("Invalid Choice")

    except ValueError:
        print("Please Enter Valid Input")
    except Exception as error:
        print(error)
