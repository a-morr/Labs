# solutions.py
"""Introductory Labs: The Standard Library. Solutions file."""

# calculator.py ===============================================================
# Students write this module as part of problem 3.

def add(x,y):
    return x + y

def mult(x,y):
    return x * y

def sqrt(x):
    return x**.5
    # or 'from math import sqrt' at the top.

# solutions.py ================================================================

import sys
from random import randint
from box import isvalid, parse_input

# Problem 1: Implement this function.
def prob1(l):
    """Accept a list 'l' of numbers as input and return a list with the
    minimum, maximum, and average of the original list (in that order).
    """
    return [min(l), max(l), float(sum(l))/len(l)]


# Problem 2: Implement this function.
def prob2():
    """Programmatically determine which Python objects are mutable and which
    are immutable. Test numbers, strings, lists, tuples, and dictionaries.
    Print your results to the terminal.
    """

    # numbers: num+= 1
    num1 = 0
    num2 = num1
    num1 += 1
    print("Numbers:\t"),
    if num1 == num2:
        print("Mutable")
    else:
        print("Immutable")

    # strings: str1 += 'a'
    str1 = "a"
    str2 = str1
    str1 += "a"
    print("Strings:\t"),
    if str1 == str2:
        print("Mutable")
    else:
        print("Immutable")

    # lists: list1.append(1)
    list1 = [4,3,2]
    list2 = list1
    list1.append(1)
    print("Lists:\t\t"),
    if list1 == list2:
        print("Mutable")
    else:
        print("Immutable")

    # tuples: tup1 += (1,)
    tup1 = (4,3,2)
    tup2 = tup1
    tup1 += (1,)
    print("Tuples:\t\t"),
    if tup1 == tup2:
        print("Mutable")
    else:
        print("Immutable")

    # dictionaries: dic1[1] = 'a'
    dic1 = dict()
    dic1[1] = 'b'
    dic2 = dic1
    dic1[1] = 'a'
    print("Dictionaries:\t"),
    if dic1 == dic2:
        print("Mutable")
    else:
        print("Immutable")


# Problem 3: Write a 'calculator' module and use it to implement this function.
def prob3(a,b):
    """Calculate and return the length of the hypotenuse of a right triangle.
    Do not use any methods other than those that are imported from your
    'calculator' module.
    Parameters:
        a : the length one of the sides of the triangle.
        b : the length the other non-hypotenuse side of the triangle.
    Returns:
        The length of the triangle's hypotenuse.
    """
    # c = calculator              # or "import calculator as c" at the top
    # return c.sqrt(c.add(c.mult(a,a),c.mult(b,b)))

    # Or, a slightly longer way:
    a2 = mult(a,a)
    b2 = mult(b,b)
    a2plusb2 = add(a2, b2)
    return sqrt(a2plusb2)


# Problem 4: Implement shut the box.
def shut_the_box():
    """Play a single game of shut the box."""

    # Get the player's name.
    if len(sys.argv) != 2:
        player = raw_input("Player name: ")
    else:
        player = sys.argv[1]

    # Initialize the box.
    numbers = range(1,10)

    # Take a turn until either the player wins or gets a game over.
    while len(numbers) > 0:
        if sum(numbers) <= 6:       # Roll a single die.
            roll = randint(1,6)
        else:                       # Roll two dice.
            roll = randint(1,6) + randint(1,6)

        # Print the game information.
        print "\nNumbers left:", numbers
        print "Roll:", roll
        if not isvalid(roll, numbers):
            print "Game over!"
            break

        # Choose a valid integer or integers to eliminate.
        choices = []
        while len(choices) == 0:
            # Parse the player's input.
            choices = parse_input(raw_input("Numbers to eliminate: "), numbers)
            # Make sure the player's choices actually sum up to the roll.
            if sum(choices) == roll:
                # Remove the player's choices from the remaining numbers.
                for number in choices:
                    numbers.remove(number)
            # Report invalid input and go back to the top of the inner loop.
            else:
                print "Invalid input"
                choices = []

    # Report the player's final score.
    score = sum(numbers)
    print("\nScore for player " + player + ": " + str(score) + " points")
    # or print("\nScore for player {}: {} points".format(player, score))
    if score == 0:
        print("Congratulations!! You shut the box!")
    print("")


if __name__ == "__main__":
    shut_the_box()

