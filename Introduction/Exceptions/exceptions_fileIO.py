# exceptions_fileIO.py
"""Introductory Labs: Exceptions and File I/O.
<Name>
<Class>
<Date>
"""


# Problem 1
def arithmagic():
    step_1 = raw_input("Enter a 3-digit number where the first and last "
                                            "digits differ by 2 or more: ")
    step_2 = raw_input("Enter the reverse of the first number, obtained "
                                            "by reading it backwards: ")
    step_3 = raw_input("Enter the positive difference of these numbers: ")
    step_4 = raw_input("Enter the reverse of the previous result: ")
    print str(step_3) + " + " + str(step_4) + " = 1089 (ta-da!)"


# Problem 2
def random_walk(max_iters=1e12):
    walk = 0
    direction = [-1, 1]
    for i in xrange(int(max_iters)):
        walk += choice(direction)
    return walk


# Problems 3 and 4: Write a 'ContentFilter' class.
