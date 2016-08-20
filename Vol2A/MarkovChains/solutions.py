# solutions.py
"""Volume II: Markov Chains. Solutions file."""

import numpy as np
# from scipy.sparse import lil_matrix
# from sklearn.preprocessing import normalize


# Problem 1
def random_markov(n):
    """Create and return a transition matrix for a random Markov chain with
    'n' states. This should be stored as an nxn NumPy array.
    """
    transition_matrix = np.random.random((n,n))
    transition_matrix /= transition_matrix.sum(axis=1)[:,np.newaxis]
    return transition_matrix


# Problem 2
def forecast(days):
    """Run a simulation for the weather over the specified number of days,
    with hot as the starting state. Return a list containing the day-by-day
    results, not including the starting day.

    Examples:
        >>> forecast(3)
        [1, 1, 0]
        >>> forecast(5)
        [0, 0, 0, 1, 0]
    """
    transition_matrix = np.array([[.7, .3], [.6, .4]])
    current_state = 0
    record = []
    for day in xrange(days):
        if np.random.random() < transition_matrix[current_state, 1]:
            current_state = 1       # Transition to cold.
        else:
            current_state = 0       # Transition to hot.
        record.append(current_state)
    return record
# Roughly 66.7% of the entries should be zeros.
# Roughly 33.3% of the entries should be ones.


# Problem 3
def four_state_forecast(days):
    """Run a simulation for the weather over the specified number of days,
    with mild as the starting state, using the four-state Markov chain.
    Return a list containing the day-by-day results, not including the
    starting day.

    Examples:
        >>> four_state_forecast(3)
        [0, 1, 3]
        >>> four_state_forecast(5)
        [2, 1, 2, 1, 1]
    """
    transition = np.array([ [.5, .3, .2, 0.],
                            [.3, .3, .3, .1],
                            [.1, .3, .4, .2],
                            [0., .3, .5, .2]    ])

    current_state = 0
    record = []
    for day in xrange(days):
        current_state = np.argmax(
                    np.random.multinomial(1, transition[current_state]))
        record.append(current_state)
    return record
# Roughly 24.6% of the entries should be zeros.
# Roughly 30.0% of the entries should be ones.
# Roughly 33.3% of the entries should be twos.
# Roughly 12.1% of the entries should be threes.


# Problem 4
# TODO: Turn this problem into an explanation of steady states.
def analyze_simulation():
    """Investigate and interpret the results of the simulations in the previous
    two problems. Specifically, find the average percentage of days that are
    hot, mild, cold, and freezing in each simulation. Does the starting day
    alter the results? Print a report of your findings (return nothing).
    """
    hot1, cold1, hot2, mild, cold2, frozen  = [], [], [], [], [], []
    for i in xrange(10):
        f2 = forecast(10000)
        f4 = four_state_forecast(10000)
        hot1.append(f2.count(0))
        cold1.append(f2.count(1))
        hot2.append(f4.count(0))
        mild.append(f4.count(1))
        cold2.append(f4.count(2))
        frozen.append(f4.count(3))
    print("2-state forecast Hot days:\t{}%".format(np.mean(hot1)/100.))
    print("2-state forecast Cold days:\t{}%".format(np.mean(cold1)/100.))
    print("4-state forecast Hot days:\t{}%".format(np.mean(hot2)/100.))
    print("4-state forecast Mild days:\t{}%".format(np.mean(mild)/100.))
    print("4-state forecast Cold days:\t{}%".format(np.mean(cold2)/100.))
    print("4-state forecast Freezing days:\t{}%".format(np.mean(frozen)/100.))


class SentenceGenerator(object):
    """Markov chain creator for simulating bad English.

    Attributes:
        (what attributes do you need to keep track of?)

    Example:
        >>> yoda = SentenceGenerator("Yoda.txt")
        >>> print yoda.babble()
        The dark side of loss is a path as one with you.
    """

    def __init__(self, filename=None):
        if filename is not None:
            self._read(filename)

    def _read(self, filename):
        """Read the specified file and build a transition matrix from its
        contents. You may assume that the file has one complete sentence
        written on each line.
        """
        self.filename = filename
        self.states = ["$tart"]

        # Initialize an empty transition matrix of the appropriate size.
        with open(self.filename, 'r') as source:
            self.num_states = len(set(source.read().split())) + 2
        self.chain = np.zeros((self.num_states, self.num_states))

        # Process the data. This assumes one sentence per line in the file.
        with open(self.filename, 'r') as source:
            for line in source:
                sentence = line.split()

                for word in sentence:
                    if word not in self.states:
                        self.states.append(word)
                indices = [self.states.index(word) for word in sentence]

                self.chain[0, indices[0]] += 1                 # &tart -> first
                for i in xrange(len(indices)-1):
                    self.chain[indices[i], indices[i+1]] += 1  # middle -> next
                self.chain[indices[-1], -1] += 1               # last -> $top

        self.chain[-1, -1] = 1.
        self.states.append("$top")

        # Make each row sum to 1.
        self.chain /= self.chain.sum(axis=1)[:,np.newaxis]

    def babble(self):
        """Begin at the start sate and use the strategy from
        four_state_forecast() to transition through the Markov chain.
        Keep track of the path through the chain and the corresponding words.
        When the stop state is reached, stop transitioning and terminate the
        sentence. Return the resulting sentence as a single string.
        """
        stop = self.num_states - 1
        path = []
        state = 0

        # Begin at the start state and end at the stop state.
        while state != stop:        # Transition to a new state...
            state = np.argmax(np.random.multinomial(1, self.chain[state]))
            if state != stop:       # ...and record the corresponding word.
                path.append(self.states[state])

        return " ".join(path)


if __name__ == '__main__':
    analyze_simulation()
    yoda = SentenceGenerator("Yoda.txt")
    for i in xrange(5):
        print yoda.babble()
