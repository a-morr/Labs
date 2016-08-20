# plots.py
"""Volume 2: Data Structures 2 (Trees). Plotting file."""
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')

import numpy as np
from time import time
from sys import stdout
from matplotlib import pyplot as plt
from solutions import iterative_search, SinglyLinkedList, BST, AVL

def prob4_plots(N=12, verbose=False):
    """At each iteration, take n random items from a pre-determined subset.

    Time (separately) how long it takes to load a SinglyLinkedList, a BST, and
    an AVL with the data set of n items.

    Choose 5 random items from the data set. Time (separately) how long it
    takes to find all 5 items in each object.

    Create two log-log figures.
    The first figure plots the number of items in each dataset against the
    build time for each object.
    The second figure, plots the number of items against the search time for
    each object.
    """

    # Initialize lists to hold results
    lls_build, lls_search = [], []
    bst_build, bst_search = [], []
    avl_build, avl_search = [], []

    data = np.random.random(2**(N+1))
    domain = 2**np.arange(3,N+1)

    # Get the values [start, start + step, ..., stop - step]
    for n in domain:
        if verbose:
            print("\rn = {}".format(n)),
            stdout.flush()

        # Initialize wordlist and data structures
        subset = data[:n]
        bst = BST()
        avl = AVL()
        lls = SinglyLinkedList()

        # Time the singly-linked list build
        begin = time()
        for item in subset:
            lls.append(item)
        lls_build.append(time() - begin)

        # Time the binary search tree build
        begin = time()
        for item in subset:
            bst.insert(item)
        bst_build.append(time() - begin)

        # Time the AVL tree build
        begin = time()
        for item in subset:
            avl.insert(item)
        avl_build.append(time() - begin)

        random_subset = np.random.choice(subset, size=5, replace=False)

        # Time the singly-linked list search
        begin = time()
        for target in random_subset:
            iterative_search(lls, target)
        lls_search.append(time() - begin)

        # Time the binary search tree search
        begin = time()
        for target in random_subset:
            bst.find(target)
        bst_search.append(time() - begin)

        # Time the AVL tree search
        begin = time()
        for target in random_subset:
            avl.find(target)
        avl_search.append(time() - begin)

    # Plot the data
    plt.clf()
    plt.title("Build Times")
    plt.loglog(domain,lls_build,'.-',lw=2,ms=10,basex=2,basey=2,label='Singly Linked List')
    plt.loglog(domain,bst_build,'.-',lw=2,ms=10,basex=2,basey=2,label='Binary Search Tree')
    plt.loglog(domain,avl_build,'.-',lw=2,ms=10,basex=2,basey=2,label='AVL Tree')
    plt.xlabel("n"); plt.ylabel("Seconds")
    plt.legend(loc='upper left')
    plt.savefig("BuildTimes.pdf")

    plt.clf()
    plt.title("Search Times")
    plt.loglog(domain,lls_search,'.-',lw=2,ms=10,basex=2,basey=2,label='Singly Linked List')
    plt.loglog(domain,bst_search,'.-',lw=2,ms=10,basex=2,basey=2,label='Binary Search Tree')
    plt.loglog(domain,avl_search,'.-',lw=2,ms=10,basex=2,basey=2,label='AVL Tree')
    plt.xlabel("n")
    plt.legend(loc='upper left')
    plt.savefig("SearchTimes.pdf")
    plt.clf()

if __name__ == '__main__':
    prob4_plots(verbose=True)
