# solutions.py
"""Introductory Labs: Exceptions and File I/O. Solutions File."""

from random import choice

# Problem 1
def arithmagic():
    step_1 = raw_input("Enter a 3-digit number where the first and last "
                                            "digits differ by 2 or more: ")
    if len(step_1) != 3:
        raise ValueError("Input must be 3 digits")
    elif abs(int(step_1[0]) - int(step_1[-1])) < 2:
        raise ValueError("First and last digit must differ by 2 or more")
    step_2 = raw_input("Enter the reverse of the first number, obtained "
                                            "by reading it backwards: ")
    if step_1 != step_2[::-1]:
        raise ValueError("Incorrect reversal")
    step_3 = raw_input("Enter the positive difference of these numbers: ")
    if int(step_3) != abs(int(step_1) - int(step_2)):
        raise ValueError("Incorrect difference")
    step_4 = raw_input("Enter the reverse of the previous result: ")
    if step_3 != step_4[::-1]:
        raise ValueError("Incorrect reversal")
    print str(step_3) + " + " + str(step_4) + " = 1089 (ta-da!)"


# Problem 2
def random_walk(max_iters=1e12):
    walk = 0
    direction = [-1, 1]
    try:
        for i in xrange(int(max_iters)):
            walk += choice(direction)
    except KeyboardInterrupt:
        print("Process Interrupted at iteration {}".format(i))
    else:
        print("Process Completed")
    return walk


class ContentFilter(object):
    """docstring for ContentFilter"""

    # Problem 3
    def __init__(self, filename):
        if not isinstance(filename, str): # or 'if type(filename) is not str:'
            raise TypeError("'filename' argument must be a string")
        self.filename = filename
        with open(filename, 'r') as f:
            self.contents = f.read()

    # Problem 4
    def uniform(self, outfile, mode='w', case='upper'):
        """Write the data ot the outfile in uniform case."""
        if mode not in {'a', 'w'}:
            raise ValueError("'mode' must be 'a' or 'w'")

        # Translate into the indicated case.
        if case == "upper":
            data = self.contents.upper()
        elif case == "lower":
            data = self.contents.lower()
        else:
            raise ValueError("'case' must be 'upper' or 'lower'")

        # Write the data.
        with open(outfile, mode) as f:
            f.write(data)

    # Problem 4
    def reverse(self, outfile, mode='w', unit='word'):
        """Write the data to the outfile in reverse order."""
        if mode not in {'a', 'w'}:
            raise ValueError("'mode' must be 'a' or 'w'")

        # Get the data into a list of lists: each inner list is a line
        # of the data, containing the words of the line.
        lines = self.contents.split('\n')
        lines = [line.split() for line in lines]

        # Perform the reversal.
        if unit == 'word':
            data = [line[::-1] for line in lines]
        elif unit == 'line':
            data = lines[::-1]
        else:
            raise ValueError("'unit' must be 'word' or 'line'")

        # Paste each line back together. Include newlines for writing.
        data = [" ".join(line) + '\n' for line in data]

        # Write the data out. Don't forget newlines!
        with open(outfile, mode) as f:
            f.writelines(data)

    # Problem 4
    def transpose(self, outfile, mode='w'):
        """Write the transposed version of the data to the outfile."""
        if mode not in {'a', 'w'}:
            raise ValueError("'mode' must be 'a' or 'w'")

        # Get the data into a list of lists as in reverse().
        lines = self.contents.split('\n')
        lines = [line.split(' ') for line in lines]

        # Calculate the max length so we can iterate.
        max_len = max([len(line) for line in lines])

        # Write the data.
        with open(outfile, mode) as f:
            for i in xrange(max_len):
                for line in lines:
                    if i < len(line):
                        f.write(line[i] + " ")
                f.write("\n")

    # Problem 4
    def __str__(self):
        """String representation: info about the contents of the file."""
        chars = len(self.contents)
        alpha = sum([s.isalpha() for s in self.contents])
        numer = sum([s.isdigit() for s in self.contents])
        space = sum([s.isspace() for s in self.contents])
        lines = len(self.contents.split('\n'))
        return "Source file:\t\t{}\nTotal characters:\t{}\nAlphabetic characters:\t{}\nNumerical characters:\t{}\nWhitespace characters:\t{}\nNumber of lines:\t{}".format(self.filename, chars, alpha, numer, space, lines)
        # Alternatively,
        out = "Source file:\t\t" + self.filename
        out += "\nTotal characters:\t" + str(chars)
        out += "\nAlphabetic characters:\t" + str(alpha)
        out += "\nNumerical characters:\t" + str(numer)
        out += "\nWhitespace characters:\t" + str(space)
        out += "\nNumber of lines:\t" + str(lines)
        return out

