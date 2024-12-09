class QuickFind:
    """
    QuickFind is a data structure for solving the dynamic connectivity problem.
    It supports union and find operations, along with connected queries.
    Attributes:
        id (list): List of integers representing the connected components.
    Methods:
        __init__(N):
            Initializes the QuickFind data structure with N elements.
        connected(p, q):
            Checks if elements p and q are in the same connected component.
        union(p, q):
            Merges the connected components containing p and q.
        find(p):
            Finds the connected component that p belongs to.
    """
    def __init__(self, N):
        self.id = list(range(N))

    def connected(self, p, q):
        """
        Check if two elements are connected.

        Parameters:
        p (int): The first element.
        q (int): The second element.

        Returns:
        bool: True if the elements are connected, False otherwise.
        """
        return self.id[p] == self.id[q]
    
    def find(self, p):
        """
        Find the identifier for the given element.

        Parameters:
        p (int): The element to find the identifier for.

        Returns:
        int: The identifier of the given element.
        """
        return self.id[p]

    def union(self, p, q):
        """
        Merges the set containing element p with the set containing element q.

        Args:
            p (int): The first element.
            q (int): The second element.
        """
        pid = self.id[p]
        qid = self.id[q]
        for i in range(len(self.id)):
            if self.id[i] == pid:
                self.id[i] = qid

class QuickUnion:
    """
    A class to represent the Quick Union data structure.
    Attributes
    ----------
    id : list
        A list where the index represents the node and the value at that index represents the parent node.
    Methods
    -------
    __init__(N):
        Initializes the Quick Union data structure with N nodes.
    root(i):
        Finds the root of node i.
    connected(p, q):
        Checks if nodes p and q are connected.
    union(p, q):
        Connects nodes p and q.
    """
    def __init__(self, N):
        """
        Initializes the UF class with N elements.

        Args:
            N (int): The number of elements.
        """
        self.id = list(range(N))

    def root(self, i):
        """
        Finds the root of the element `i` in the union-find data structure.

        This method follows the chain of parent pointers from the element `i` 
        up the tree until it reaches the root element, which is an element 
        that is its own parent.

        Args:
            i (int): The element for which to find the root.

        Returns:
            int: The root of the element `i`.
        """
        while i != self.id[i]:
            i = self.id[i]
        return i

    def connected(self, p, q):
        """
        Check if two elements are connected.

        This method determines if the two elements `p` and `q` are in the same connected component.

        Args:
            p (int): The first element.
            q (int): The second element.

        Returns:
            bool: True if the elements `p` and `q` are connected, False otherwise.
        """
        return self.root(p) == self.root(q)

    def union(self, p, q):
        """
        Perform the union operation on two elements p and q.
        
        Args:
            p (int): The first element.
            q (int): The second element.
        """
        i = self.root(p)
        j = self.root(q)
        self.id[i] = j


class WeightedQuickUnion:
    """
    A data structure for union-find with weighted quick union.

    This class implements the union-find algorithm with path compression
    and weighting to ensure efficient union and find operations.

    Attributes:
        id (list): The list to hold the parent of each element.
        sz (list): The list to hold the size of each tree.
        count (int): The number of components.

    Methods:
        __init__(N):
            Initializes the UF object with N elements.
        root(i):
            Finds the root of the element at index i in the Union-Find data structure.
        connected(p, q):
            Determines whether two elements are connected in the union-find data structure.
        union(p, q):
            Unites two elements by connecting their roots.
        size(i):
            Returns the size of the component that the element 'i' belongs to.
        count():
            Returns the number of components in the union-find data structure.
    """
    def __init__(self, N):
        """
        Initializes the UF object with N elements.

        Parameters:
        - N (int): The number of elements in the UF object.

        Returns:
        None
        """
        self.id = list(range(N))
        self.sz = [1] * N
        self.count = N

    def root(self, i):
        """
        Finds the root of the element at index i in the Union-Find data structure.

        Parameters:
        - i: The index of the element.

        Returns:
        - The root of the element at index i.

        Notes:
        - This method uses path compression to optimize the search for the root.
        """
        while i != self.id[i]:
            self.id[i] = self.id[self.id[i]]  # path compression
            i = self.id[i]
        return i

    def connected(self, p, q):
        """
        Determines whether two elements are connected in the union-find data structure.

        Parameters:
            p (int): The first element.
            q (int): The second element.

        Returns:
            bool: True if the elements are connected, False otherwise.
        """
        return self.root(p) == self.root(q)

    def union(self, p, q):
        """
        Unites two elements by connecting their roots.
        Parameters:
        - p: The first element.
        - q: The second element.
        Returns:
        None
        """
        i = self.root(p)
        j = self.root(q)
        if i == j:
            return

        if self.sz[i] < self.sz[j]:
            self.id[i] = j
            self.sz[j] += self.sz[i]
        else:
            self.id[j] = i
            self.sz[i] += self.sz[j]
        
        self.count -= 1
    
    def size(self, i):
        """
        Returns the size of the component that the element 'i' belongs to.

        Parameters:
        - i: The element for which the size of the component is to be determined.

        Returns:
        - The size of the component that the element 'i' belongs to.
        """
        return self.sz[self.root(i)]
    
    def count(self):
        """
        Returns the number of components in the union-find data structure.

        Parameters:
        None

        Returns:
        int: The number of components in the union-find data structure.
        """
        return self.count