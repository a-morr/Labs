# solutions.py
"""Volume 2A: Breadth-First Search (Kevin Bacon). Solutions file."""

from collections import deque
import networkx as nx
from matplotlib import pyplot as plt


# Problems 1-4: Implement the following class
class Graph(object):
    """A graph object, stored as an adjacency dictionary. Each node in the graph is a key in the dictionary.
    The value of each key is a list of the corresponding node's neighbors.
    """

    def __init__(self, adjacency):
        """Store the adjacency dictionary as a class attribute"""
        self.dictionary = adjacency

    # Problem 1
    def __str__(self):
        """String representation: a sorted view of the adjacency dictionary.

        Example:
            >>> test = {'A':['D', 'C', 'B'], 'D':['A', 'C'],
            ...         'C':['B', 'A', 'D'], 'B':['A', 'C']}
            >>> print(Graph(test))
            A: B; C; D
            B: A; C
            C: A; B; D
            D: A; C
        """
        out = ""
        keys = self.dictionary.keys()
        keys.sort()
        # join() approach
        for key in keys:
            out += str(key) + ": "              # add each node
            values = self.dictionary[key]
            values.sort()
            out += "; ".join(values) + "\n"     # add the node's neighborhood
        return out
        # for loop approach
        for key in keys:
            out += str(key) + ": "              # add each node
            values = self.dictionary[key]
            values.sort()
            for value in values:                # add each neighbor
                out += str(value) + "; "
            out = out.strip("; ") + "\n"        # strip off the last "; "
        return out

    # Problem 2
    def traverse(self, start):
        """Begin at 'start' and perform a breadth-first search until all
        nodes in the graph have been visited. Return a list of values,
        in the order that they were visited. If 'start' is not in the
        adjacency dictionary, raise a ValueError.

        Inputs:
            start: the node to start the search at.

        Returns:
            the list of visited nodes (in order of visitation)

        Example:
            >>> test = {'A':['B'], 'B':['A', 'C',], 'C':['B']}
            >>> Graph(test).traverse('B')
            ['B', 'A', 'C']
        """

        # Validate input
        if start not in self.dictionary:
            raise ValueError(str(start) + " is not in the graph.")

        # Set up the data structures
        visited = list()
        marked = set(start)
        visit_queue = deque(start)

        # Search the graph until done:
        while len(visit_queue) > 0:
            # get the next node from the queue and visit it
            current = visit_queue.popleft()
            visited.append(current)

            # put any unvisited, unmarked neighbors of the
            # current node on the visiting queue
            for neighbor in self.dictionary[current]:
                if neighbor not in marked:
                    visit_queue.append(neighbor)
                    marked.add(neighbor)
        return visited

    # Problem 3 (Optional)
    def DFS(self, start):
        """Begin at 'start' and perform a depth-first search until all
        nodes in the graph have been searched. Return a list of values, in
        the order that they were visited. If 'start' is not in the
        adjacency dictionary, raise a ValueError.

        Inputs:
            start: the node to start the search at.

        Returns:
            the list of visited nodes (in order of visitation)

        Example:
            >>> test = {'A':['B', 'D'], 'B':['A', 'C'],
            ...         'C':['B', 'D'], 'D':['A', 'C']}
            >>> Graph(test).DFS('A')
            ['A', 'B', 'C', 'D']
        """
        if start not in self.dictionary:
            raise ValueError(str(start) + " is not in the graph.")

        visited = list()
        marked = set(start)
        visit_queue = deque(start)          # for DFS, use this as a stack

        while len(visit_queue) > 0:
            current = visit_queue.pop()     # This line is different from BFS
            visited.append(current)
            for neighbor in self.dictionary[current]:
                if neighbor not in marked:
                    visit_queue.append(neighbor)
                    marked.add(neighbor)
        return visited

    # Problem 4
    def shortest_path(self, start, target):
        """Begin at the node containing 'start' and perform a breadth-first
        search until the node containing 'target' is found. Return a list
        containg the shortest path from 'start' to 'target'. If either of
        the inputs are not in the adjacency graph, raise a ValueError.

        Inputs:
            start: the node to start the search at.
            target: the node to search for.

        Returns:
            A list of nodes along the shortest path from start to target,
                including the endpoints.

        Example:
            >>> test = {'A':['B', 'F'], 'B':['A', 'C'], 'C':['B', 'D'],
            ...         'D':['C', 'E'], 'E':['D', 'F'], 'F':['A', 'E', 'G'],
            ...         'G':['A', 'F']}
            >>> Graph(test).shortest_path('A', 'G')
            ['A', 'F', 'G']
        """
        if start not in self.dictionary:
            raise ValueError("Starting point " + str(start)
                                    + " is not in the graph.")
        # if target not in self.dictionary: raise ValueError

        visited = list()
        marked = set(start)
        visit_queue = deque(start)
        all_paths = {}
        final_path = deque()

        while len(visit_queue) > 0:
            current = visit_queue.popleft()
            visited.append(current)

            # Check for the target
            if current == target:
                # Build the shortest path
                final_path.append(current)
                while current in all_paths:
                    final_path.appendleft(all_paths[current])
                    current = all_paths[current]
                return list(final_path)
            # Otherwise continue as before
            else:
                for neighbor in self.dictionary[current]:
                    if neighbor not in marked:
                        visit_queue.append(neighbor)
                        marked.add(neighbor)
                        # Track the path
                        all_paths[neighbor] = current

        # If all neighbors have been checked, the target isn't in the graph.
        raise ValueError("Target " + str(target) + " is not in the graph.")

    def cheater(self, start, target):
        return nx.shortest_path(
            convert_to_networkx(self.dictionary), start, target)


# Problem 5: Write the following function
def convert_to_networkx(dictionary):
    """Convert 'dictionary' to a networkX object and return it."""
    # Make the graph
    output = nx.Graph()
    for key in dictionary:
        for value in dictionary[key]:
            # Add each edge. Duplicates are automatically ignored.
            output.add_edge(key, value)
    return output


# Helper function for problem 6
def parse(filename="movieData.txt"):
    """Generate an adjacency dictionary where each key is
    a movie and each value is a list of actors in the movie.
    """

    # open the file, read it in, and split the text by '\n'
    movieFile = open(filename, 'r')
    movieFile = movieFile.read()
    movieFile = movieFile.split('\n')
    graph = dict()

    # for each movie in the file,
    for line in movieFile:
        # get movie name and list of actors
        names = line.split('/')
        movie = names[0]
        graph[movie] = []
        # add the actors to the dictionary
        for actor in names[1:]:
            graph[movie].append(actor)

    return graph


# Problems 6-8: Implement the following class
class BaconSolver(object):
    """Class for solving the Kevin Bacon problem."""

    # Problem 6
    def __init__(self, filename="movieData.txt"):
        """Initialize the networkX graph and with data from the specified
        file. Store the graph as a class attribute. Also store the collection
        of actors in the file as a class attribute.
        """
        # Get the adjacency dictionary from the file
        movie_to_actors = parse(filename)

        # Extract the actors from the adjacency dictionary (values)
        self.actors = set()
        for movie in movie_to_actors:
            for actor in movie_to_actors[movie]:
                self.actors.add(actor)

        # Convert the adjacency matrix to networkX
        self.bacon_graph = convert_to_networkx(movie_to_actors)

    # Problem 6
    def path_to_bacon(self, start, target="Bacon, Kevin"):
        """Find the shortest path from 'start' to 'target'."""
        if start not in self.actors:
            raise ValueError(str(start) + " is not in the set of actors")
        if target not in self.actors:
            raise ValueError(str(target) + " is not in the set of actors")
        return nx.shortest_path(self.bacon_graph, start, target)

    # Problem 7
    def bacon_number(self, start, target="Bacon, Kevin"):
        """Return the Bacon number of 'start'."""
        # Integer divide by two to account for movies in the path.
        return len(self.path_to_bacon(start, target)) // 2

    # Problem 7
    def average_bacon(self, target="Bacon, Kevin"):
        """Calculate the average Bacon number in the data set.
        Note that actors are not guaranteed to be connected to the target.
        """
        connected = 0
        isolated = 0
        total = 0
        for actor in self.actors:
            # if nx.has_path(self.bacon_graph, actor, target):
            try:
                total += self.bacon_number(actor, target)
                connected += 1
            except nx.NetworkXNoPath:
                isolated += 1

        return float(total)/connected, isolated

    # Problem 8 (Optional)
    def plot_bacon(self, target="Bacon, Kevin"):
        """Create and show a histogram displaying the frequency of the Bacon
        numbers in the data set. Ignore entries with no path to 'target'.
        """
        bacon = deque()
        for actor in self.actors:
            try:
                bacon.append(self.bacon_number(actor, target))
            except nx.NetworkXNoPath:
                pass
        name = target.partition(",")[0]
        plt.hist(bacon, bins=7)
        plt.title(name + " Number Distribution")
        plt.xlabel(name + " Number")
        plt.ylabel("Actors")
        plt.show()

