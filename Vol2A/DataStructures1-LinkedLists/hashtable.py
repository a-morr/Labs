class HashTable(object):
    def __init__(self, size, hashfun, thresh=.75):
        # Allocating a list of nones
        self.hashtable = [None]*size
        self.size = size
        self.len = 0
        self.thresh = thresh
        # Hash function (define your function outside of the class, anything that defines a call method is callable)
        self._hash = hashfun
        # Ascertains that the load attribute is defined.
        self._update_load()

    def __len__(self):
        return self.len

    def _update_load(self):
        self.load = float(self.len)/self.size

    def __iter__(self):
        for b in self.hashtable:
            if b is not None:
                for i in b:
                    yield i

    def load(self):
        self._update_load()
        return self.load

    def _insert(self, data, hashtable, hashsize):
        hx = self._hash(data[0], hashsize)
        try:
            found = False
            for i, v in enumerate(hashtable[hx]):
                if v[0] == data[0]:
                    found = True
                    break
            if found:
                hashtable[hx][i] = data
            else:
                hashtable[hx].append(data)
        except (AttributeError, TypeError):
            hashtable[hx] = [data]

    def insert(self, data):
        self._insert(data, self.hashtable, self.size)
        self.len += 1
        self._update_load()

        if self.load > self.thresh:
            self._realloc(self.size*2)

    def _realloc(self, newsize):
        newhash = [None]*newsize

        for i in iter(self):
            self._insert(i, newhash, newsize)

        self.hashtable = newhash
        self.size = newsize
        self._update_load()

    def find(self, key):
        hx =  self._hash(key, self.size)
        try:
            found = False
            for i, v in enumerate(self.hashtable[hx]):
                if v[0] == key:
                    return v[1]
        except ValueError:
            raise

    def remove(self, data):
        hx = self._hash(data[0])
        try:
            self.hashtable[hx].remove(data)
        except ValueError:
            raise

class HashTable(object):
    """Hash Table Class.
    
    Attributes:
        table (list): the actual hash table. Each element is a list.
        size (int): the number of items in the hash table.
        capacity (int): the maximum number of items in the table.
    
    Notes:
        Do not allow a table of capacity 0 to be initialized.
        Use the built-in Python hash function.
        Handle hash collisions by chaining.
        If the load factor exceeds 0.8, reset the table's capacity so that
            the load factor drops below 0.2.
    """
    def __init__(self,capacity=4):
        if capacity <= 0: capacity = 1      # No empty tables allowed
        self.table = [list() for i in range(capacity)]
        self.capacity = capacity
        self.size = 0
    
    def load_factor(self):
        """Return the percent of the hash table that is occupied."""
        return float(self.size)/self.capacity   # Use float division!
    
    def resize(self,new_capacity):
        new_table = [list() for i in range(new_capacity)] # New blank table
        for i in self.table:            # For each entry in the table (a list)
            for j in i:                 # For each entry in that list
                new_table[hash(j)%new_capacity].append(j) # Rehash
        self.table = new_table          # Store the new table
        self.capacity = new_capacity    # Reset the capacity
    
    def insert(self,data):
        """Add a single element to the hash table."""
        self.table[hash(data) % self.capacity].append(data) # Add data
        self.size += 1                                      # Adjust size
        if self.load_factor() > .8 or self.size >= self.capacity:
            self.resize(self.capacity * 4)                  # Resize if needed
    
    def __str__(self):
        """String representation: table contents and load factor."""
        out = str(self.table)
        out += "\nLoad Factor: " + str(self.load_factor())
        return out
