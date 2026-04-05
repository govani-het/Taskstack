class Stack:
    """
        Represents a stack data structure.

        Parameters:
        capacity (int): Maximum number of elements allowed in the stack.

        Returns:
        None
    """

    def __init__(self, capacity):
        """
            Initializes a stack instance.

            Parameters:
            capacity (int): Maximum size of stack.

            Returns:
            None
        """
        self.items = []
        self.capacity = capacity

    def push(self, item):
        """
            Inserts an element at the top of the stack.

            Parameters:
            item (Any): Value to push into stack.

            Returns:
            None
        """
        if self.is_full():
            print("Stack is Full")
        else:
            self.items += [item]

    def pop(self):
        """
            Removes and returns the top element of the stack.

            Parameters:
            None

            Returns:
            Any | None: The removed top element, or None when stack is empty.
        """
        if self.is_empty():
            print("Stack is Empty")
            return None

        popped_value = self.items[-1]
        del self.items[-1]
        print(f"Popped: {popped_value}")
        return popped_value

    def peek(self):
        """
            Displays the current top element.

            Parameters:
            None

            Returns:
            None
        """
        if self.is_empty():
            print("Stack is Empty")
        else:
            print(self.items[-1])

    def display(self):
        """
            Displays all current stack elements.

            Parameters:
            None

            Returns:
            None
        """
        if self.is_empty():
            print("Stack is Empty")
        else:
            print(self.items)

    def is_empty(self):
        """
            Checks whether the stack has no elements.

            Parameters:
            None

            Returns:
            bool: True when stack is empty, else False.
        """
        return len(self.items) == 0

    def is_full(self):
        """
            Checks whether the stack reached maximum capacity.

            Parameters:
            None

            Returns:
            bool: True when stack is full, else False.
        """
        return len(self.items) == self.capacity


def create_stack():
    """
        Reads stack size from user and creates stack object.

        Parameters:
        None

        Returns:
        Stack: Created stack instance.
    """
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
    """
        Handles stack menu operations.

        Parameters:
        stack (Stack): Stack instance used for operations.

        Returns:
        None
    """
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
                try:
                    if "." in raw_item:
                        item = float(raw_item)
                    else:
                        item = int(raw_item)
                except ValueError:
                    item = raw_item
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


if __name__ == "__main__":
    stack = create_stack()
    handle_stack_operations(stack)
