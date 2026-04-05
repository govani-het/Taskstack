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
        """Remove and return the top value from the stack."""
        if self.is_empty():
            print("Stack is Empty")
            return None

        popped_value = self.items[-1]
        del self.items[-1]
        print(f"Popped: {popped_value}")
        return popped_value

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


def parse_input_value(raw_value):
    """Convert numeric text to number, otherwise keep as string."""
    try:
        if "." in raw_value:
            return float(raw_value)
        return int(raw_value)
    except ValueError:
        return raw_value


def create_stack():
    """Read stack size and create a stack instance."""
    while True:
        try:
            stack_size = int(input("Enter size of stack:- "))
            if stack_size <= 0:
                print("Please Enter Positive Number or Greater than 0")
            else:
                return Stack(stack_size)
        except ValueError:
            print("Please Enter Valid Input")


def handle_stack_operations(stack):
    """Handle stack menu operations."""
    should_continue = True

    while should_continue:
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
                raw_item = input("Enter value to Push:- ")
                item = parse_input_value(raw_item)
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
                should_continue = False

            else:
                print("Invalid Choice")

        except ValueError:
            print("Please Enter Valid Input")
        except Exception as error:
            print(f"Error: {error}")
def main():
    """Program entry point."""
    stack = create_stack()
    handle_stack_operations(stack)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Unexpected error: {error}")
