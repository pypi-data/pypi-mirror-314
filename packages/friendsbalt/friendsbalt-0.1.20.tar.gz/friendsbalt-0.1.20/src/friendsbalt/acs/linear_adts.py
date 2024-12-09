import random
import warnings

class Queue:
    """
    A class representing a queue data structure.
    
    Methods:
        __init__():
            Initializes an empty queue.
        isEmpty():
            Checks if the queue is empty.
        enqueue(item):
            Adds an item to the queue.
        dequeue():
            Removes and returns the item from the front of the queue.
        size():
            Returns the number of items in the queue.
        __iter__():
            Returns an iterator for the queue.
        __next__():
            Returns the next item in the queue during iteration.
    """
    def __init__(self):
        self.items = []

    def isEmpty(self):
        """
        Deprecated: Use is_empty() instead.
        """
        warnings.warn(
            "isEmpty() is deprecated, use is_empty() instead",
            DeprecationWarning,
            stacklevel=2
        )
        return self.items == []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    def __iter__(self):
        self.index = 0
        return self
    def __next__(self):
        if self.index == len(self.items):
            raise StopIteration
        self.index += 1
        return self.items[self.index-1]

class Stack:
    """
    Stack Abstract Data Structure
    
    Methods:
        __init__():
            Initializes an empty stack.
        isEmpty():
            Checks if the stack is empty.
        push(item):
            Adds an item to the top of the stack.
        pop():
            Removes and returns the item from the top of the stack.
        peek():
            Returns the item from the top of the stack without removing it.
        size():
            Returns the number of items in the stack.
        __iter__():
            Returns an iterator for the stack.
        __next__():
            Returns the next item from the stack during iteration.
    """

    def __init__(self):
        self.items = []

    def isEmpty(self):
        """
        Deprecated: Use is_empty() instead.
        """
        warnings.warn(
            "isEmpty() is deprecated, use is_empty() instead",
            DeprecationWarning,
            stacklevel=2
        )
        return self.items == []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self, index=1):
        """
        Returns the item at the given index from the end of the list without removing it.

        Args:
            index (int): The position from the end of the list to peek at. Defaults to 1.

        Returns:
            object: The item at the specified index from the end of the list.

        Raises:
            IndexError: If the index is out of range.
        """
        return self.items[-index]

    def size(self):
        return len(self.items)
    
    def __iter__(self):
        self.index = len(self.items)
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.items[self.index]
    
    def __repr__(self):
        return f"Stack({self.items})"

class Deque:
    """
    A class representing a deque data structure.
    
    Methods:
        __init__():
            Initializes an empty deque.
        isEmpty():
            Checks if the deque is empty.
        addFront(item):
            Adds an item to the front of the deque.
        addRear(item):
            Adds an item to the rear of the deque.
        removeFront():
            Removes and returns the item from the front of the deque.
        removeRear():
            Removes and returns the item from the rear of the deque.
        size():
            Returns the number of items in the deque.
        __iter__():
            Returns an iterator for the deque.
        __next__():
            Returns the next item in the deque during iteration.
    """
    def __init__(self):
        self.items = []

    def isEmpty(self):
        """
        Deprecated: Use is_empty() instead.
        """
        warnings.warn(
            "isEmpty() is deprecated, use is_empty() instead",
            DeprecationWarning,
            stacklevel=2
        )
        return self.items == []
    
    def is_empty(self):
        return self.items == []

    def addFront(self, item):
        self.items.append(item)

    def addRear(self, item):
        self.items.insert(0,item)

    def removeFront(self):
        return self.items.pop()

    def removeRear(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)
    
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index == len(self.items):
            raise StopIteration
        self.index += 1
        return self.items[self.index-1]
    
class Bag:
    """
    A class representing a bag data structure.
    
    Methods:
        __init__():
            Initializes an empty bag.
        is_empty():
            Checks if the bag is empty.
        add(item):
            Adds an item to the bag.
        size():
            Returns the number of items in the bag.
        __iter__():
            Returns an iterator for the bag.
        __next__():
            Returns the next item in the bag during iteration.
    """
    def __init__(self):
        self.items = []

    def isEmpty(self):
        """
        Deprecated: Use is_empty() instead.
        """
        warnings.warn(
            "isEmpty() is deprecated, use is_empty() instead",
            DeprecationWarning,
            stacklevel=2
        )
        return self.items == []
    
    def is_empty(self):
        return self.items == []

    def add(self, item):
        self.items.append(item)

    def size(self):
        return len(self.items)
    
    def __iter__(self):
        self.random_items = self.items[:]
        random.shuffle(self.random_items)
        self.index = 0
        return self

    def __next__(self):
        if self.index == len(self.random_items):
            raise StopIteration
        self.index += 1
        return self.random_items[self.index-1]