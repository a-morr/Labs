# solutions.py
"""Volume II Lab 4: Data Structures 1 (Linked Lists). Solutions file."""


# Problem 1: Modify the constructor of the Node class.
class Node(object):
    """A basic node class for storing data."""
    def __init__(self, data):
        """Store 'data' in the 'value' attribute.

        Raises:
            TypeError: if 'data' is not of type int, long, float, or str.
        """
        if type(data) not in {int, long, float, str}:
            raise TypeError("Invalid data type: {}".format(type(data)))
        self.value = data


class LinkedListNode(Node):
    """A node class for doubly linked lists. Inherits from the 'Node' class.
    Contains references to the next and previous nodes in the linked list.
    """
    def __init__(self, data):
        """Store 'data' in the 'value' attribute and initialize
        attributes for the next and previous nodes in the list.
        """
        Node.__init__(self, data)       # Use inheritance to set self.value.
        self.next = None
        self.prev = None


class LinkedList(object):
    """Doubly linked list data structure class.

    Attributes:
        head (LinkedListNode): the first node in the list.
        tail (LinkedListNode): the last node in the list.
    """
    def __init__(self):
        """Initialize the 'head' and 'tail' attributes by setting
        them to 'None', since the list is empty initially.
        """
        self.head = None
        self.tail = None
        self._size = 0                              # for __len__()

    def append(self, data):
        """Append a new node containing 'data' to the end of the list."""
        # Create a new node to store the input data.
        new_node = LinkedListNode(data)
        if self.head is None:
            # If the list is empty, assign the head and tail attributes to
            # new_node, since it becomes the first and last node in the list.
            self.head = new_node
            self.tail = new_node
        else:
            # If the list is not empty, place new_node after the tail.
            self.tail.next = new_node               # tail --> new_node
            new_node.prev = self.tail               # tail <-- new_node
            # Now the last node in the list is new_node, so reassign the tail.
            self.tail = new_node
        self._size += 1                             # for __len__()

    # Problem 2
    def find(self, data):
        """Return the first node in the list containing 'data'.
        If no such node exists, raise a ValueError.

        Examples:
            >>> l = LinkedList()
            >>> for i in [1,3,5,7,9]:
            ...     l.append(i)
            ...
            >>> node = l.find(5)
            >>> node.data
            5
            >>> l.find(10)
            ValueError: <message>
        """
        current = self.head                 # Start at the head.
        while current is not None:          # Iterate through each node.
            if current.value == data:       # Check for the data.
                return current              # Return node if found; if not
            current = current.next          #  found, raise a ValueError.
        raise ValueError("{} is not in the list".format(data))

    # Problem 3
    def __len__(self):
        """Return the number of nodes in the list.

        Examples:
            >>> l = LinkedList()
            >>> for i in [1,3,5]:
            ...     l.append(i)
            ...
            >>> len(l)
            3
            >>> l.append(7)
            >>> len(l)
            4
        """
        return self._size

    # Problem 3
    def __str__(self):
        """String representation: the same as a standard Python list.

        Examples:
            >>> l1 = LinkedList()   |   >>> l2 = LinkedList()
            >>> for i in [1,3,5]:   |   >>> for i in ['a','b',"c"]:
            ...     l1.append(i)    |   ...     l2.append(i)
            ...                     |   ...
            >>> print(l1)           |   >>> print(l2)
            [1, 3, 5]               |   ['a', 'b', 'c']
        """
        # List construction method (recommended).
        current = self.head
        items = []
        while current is not None:
            items.append(current.value)
            current = current.next
        return str(items)

        # String construction method.
        current = self.head
        out = "["
        while current is not None:
            if isinstance(current.value, str):
                item = "'" + str(current.value) + "'"
            else:
                item = str(current.value)
            out += item
            current = current.next
            if current is not None:
                out += ", "
        out += "]"
        return out

    # Problem 4
    def remove(self, data):
        """Remove the first node in the list containing 'data'. Return nothing.

        Raises:
            ValueError: if the list is empty, or does not contain 'data'.

        Examples:
            >>> print(l1)       |   >>> print(l2)
            [1, 3, 5, 7, 9]     |   [2, 4, 6, 8]
            >>> l1.remove(5)    |   >>> l2.remove(10)
            >>> l1.remove(1)    |   ValueError: <message>
            >>> l1.remove(9)    |   >>> l3 = LinkedList()
            >>> print(l1)       |   >>> l3.remove(10)
            [3, 7]              |   ValueError: <message>
        """
        target = self.find(data)            # Raise the ValueError if needed.
        if self.head is self.tail:          # Case 1: remove only node.
            self.head = None                    # reassign the head.
            self.tail = None                    # reassign the tail.
        elif target is self.head:           # Case 1: remove the head.
            self.head = self.head.next          # reassign the head.
            self.head.prev = None               # target <-/- head
        elif target is self.tail:           # Case 2: remove the tail.
            self.tail = self.tail.prev          # reassign the tail.
            self.tail.next = None               # tail -/-> target
        else:                               # Case 3: remove from middle.
            target.prev.next = target.next      # -/-> target
            target.next.prev = target.prev      # target <-/-
        self._size -= 1                     # for __len__()

    # Problem 5
    def insert(self, data, place):
        """Insert a node containing 'data' immediately before the first node
        in the list containing 'place'. Return nothing.

        Raises:
            ValueError: if the list is empty, or does not contain 'place'.

        Examples:
            >>> print(l1)           |   >>> print(l1)
            [1, 3, 7]               |   [1, 3, 5, 7, 7]
            >>> l1.insert(7,7)      |   >>> l1.insert(3, 2)
            >>> print(l1)           |   ValueError: <message>
            [1, 3, 7, 7]            |
            >>> l1.insert(5,7)      |   >>> l2 = LinkedList()
            >>> print(l1)           |   >>> l2.insert(10,10)
            [1, 3, 5, 7, 7]         |   ValueError: <message>
        """
        after = self.find(place)            # Raise the ValueError if needed.
        new_node = LinkedListNode(data)      # Make the new node.
        if after is self.head:              # Case 1: insert before the head.
            new_node.next = self.head           # new --> head
            self.head.prev = new_node           # new <-- head
            self.head = new_node                # reassign the head.
        else:                               # Case 2: insert to middle.
            after.prev.next = new_node          # before --> new
            new_node.prev = after.prev          # before <-- new
            new_node.next = after               # new --> after
            after.prev = new_node               # new <-- after
        self._size += 1                     # for __len__()


# Problem 6
class Deque(LinkedList):
    """Deque doubly linked list data structure class.

    Attributes:
        head (LinkedListNode): the first node in the list.
        tail (LinkedListNode): the last node in the list.
    """
    def pop(self):
        """Remove the last node in the list and return its value."""
        if self.tail is None:               # Case 1: Empty list.
            raise ValueError("The list is empty")
        else:                               # Case 2: Nonempty list.
            data = self.tail.value
            LinkedList.remove(self, data)
            return data

    def popleft(self):
        """Remove the first node in the list and return its value."""
        if self.head is None:               # Case 1: Empty list.
            raise ValueError("The list is empty")
        else:                               # Case 2: Nonempty list.
            data = self.head.value
            LinkedList.remove(self, data)
            return data

    def appendleft(self, data):
        """Place a new node containing 'data' at the beginning of the list."""
        if self.head is None:               # Case 1: Empty list.
            LinkedList.append(self, data)
        else:                               # Case 2: Nonempty list.
            LinkedList.insert(self, data, self.head.value)

    def remove(*args, **kwargs):
        raise NotImplementedError("Use pop() or popleft() for removal")

    def insert(*args, **kwargs):
        raise NotImplementedError("Use append() or appendleft() for insertion")


# Problem 7
def prob7(infile, outfile):
    """Reverse the file 'infile' by line and write the results to 'outfile'."""
    with open(infile, 'r') as f:            # Read the lines in as a list.
        lines = f.readlines()
    deque = Deque()                         # Instantiate a deque.
    for line in lines:                      # Add each line to the deque.
        deque.append(line)
    with open(outfile, 'w') as f:           # Write to the outfile in reverse.
        while deque.head is not None:
            f.write(str(deque.pop()))


# Additional Material =========================================================

class SortedList(LinkedList):
    """Sorted doubly linked list data structure class.
    Inherits from the 'LinkedList' class.

    Attributes:
        head (LinkedListNode): the first node in the list.
        tail (LinkedListNode): the last node in the list.
    """

    def add(self, data):
        """Create a new Node containing 'data' and insert it at the
        appropriate location to preserve list sorting.
        """
        if self.head is None:               # Case 1: Empty list.
            LinkedList.append(self, data)
        elif self.tail.value <= data:       # Case 2: Append after the tail.
            LinkedList.append(self, data)
        else:                               # Case 3: Insert to middle.
            current = self.head
            while current.value < data:         # Find insertion location.
                current = current.next
            LinkedList.insert(self, data, current.value)

    def append(*args, **kwargs):
        raise NotImplementedError("append() is disabled (use add())")

    def insert(*args, **kwargs):
        raise NotImplementedError("insert() is disabled (use add())")

