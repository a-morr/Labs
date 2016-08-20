# solutions.py
"""Introductory Labs: Object Oriented Programming. Solutions file."""

from math import sqrt

class Backpack(object):
    """Backpack object. Has a name, color, maximum size,
    and a list of contents.

    Attributes:
        name (str): the name of the backpack's owner.
        color (str): the color of the backpack.
        max_size (int): the maximum number of items that can fit
            in the backpack.
        contents (list): the contents of the backpack.
    """

    # Problem 1
    def __init__(self, name, color, max_size=5):
        """Set the color, name, and maximum size of the backpack.
        Also initialize an empty contents list.

        Inputs:
            name (str): the name of the backpack's owner.
            color (str): the color of the backpack.
            max_size (int): the maximum number of items that can fit
                in the backpack.

        Returns:
            A backpack object wth no contents.
        """
        self.name, self.color, self.max_size = name, color, max_size
        self.contents = []

    # Problem 1
    def put(self,item):
        """Add 'item' to the backpack's list of contents if there is room."""
        if len(self.contents) >= self.max_size:         # Check for overflow.
            print("No Room!")
        else:
            self.contents.append(item)

    def take(self, item):
        """Remove 'item' from the backpack's list of contents."""
        self.contents.remove(item)

    # Problem 1
    def dump(self):
        """Remove all items from the backpack."""
        self.contents = []

    # Magic Methods -----------------------------------------------------------

    def __add__(self, other):
        """Add the number of contents of each Backpack."""
        return len(self.contents) + len(other.contents)

    def __lt__(self, other):
        """Compare two backpacks. If 'self' has fewer contents
        than 'other', return True. Otherwise, return False.
        """
        return len(self.contents) < len(other.contents)

    # Problem 3
    def __eq__(self, other):
        """Two backpack objects are equal if and only if they have the same
        name, color, and number of contents.
        """
        return self.name == other.name and self.color == other.color and len(
                                        self.contents) == len(other.contents)

    # Problem 3
    def __str__(self):
        """String Representation: a list of the backpack's attributes."""
        return "Owner:\t\t{}\nColor:\t\t{}\nSize:\t\t{}\nMax Size:\t{}\nContents:\t{}".format(self.name, self.color, len(self.contents),
                                                self.max_size, self.contents)
        # Or, a slightly longer way:
        out = "Owner:\t\t" + self.name
        out += "\nColor:\t\t" + self.color
        out += "\nSize:\t\t" + str(len(self.contents))
        out += "\nMax Size:\t" + str(self.max_size)
        out += "\nContents:\t" + str(self.contents)
        return out


# An example of inheritance. You are not required to modify this class.
class Knapsack(Backpack):
    """A Knapsack object class. Inherits from the Backpack class.
    A knapsack is smaller than a backpack and can be tied closed.

    Attributes:
        name (str): the name of the knapsack's owner.
        color (str): the color of the knapsack.
        max_size (int): the maximum number of items that can fit
            in the knapsack.
        contents (list): the contents of the backpack.
        closed (bool): whether or not the knapsack is tied shut.
    """

    def __init__(self, name, color, max_size=3):
        """Use the Backpack constructor to initialize the name and
        max_size attributes. A knapsack only holds 3 item by default
        instead of 5.

        Inputs:
            name (str): the name of the knapsack's owner.
            color (str): the color of the knapsack.
            max_size (int, opt): the maximum number of items that can be
                stored in the knapsack. Defaults to 3.

        Returns:
            A knapsack object with no contents.
        """

        Backpack.__init__(self, name, color, max_size)
        self.closed = True

    def put(self, item):
        """If the knapsack is untied, use the Backpack.put() method."""
        if self.closed:
            print "I'm closed!"
        else:
            Backpack.put(self, item)

    def take(self, item):
        """If the knapsack is untied, use the Backpack.take() method."""
        if self.closed:
            print "I'm closed!"
        else:
            Backpack.take(self, item)


# Problem 2
class Jetpack(Backpack):
    """A Jetpack object class. Inherits from the Backpack class.
    In addition to storing items like a backpack, a jetpack has
    fuel that is used to fly.

    Attributes:
        name (str): the name of the jetpack's owner.
        color (str): the color of the jetpack.
        max_size (int): the maximum number of items that can fit
            in the jetpack.
        contents (list): the contents of the jetpack.
        fuel (int): the amount of fuel in the jetpack's tank.
    """

    def __init__(self, name, color, max_size=2, fuel=10):
        """Constructor for a jetpack object. A jetpack only holds 2 items
        by default instead of 5, and has an additional attribute for fuel.

        Inputs:
            name (str): the name of the jetpack's owner.
            color (str): the color of the jetpack.
            max_size (int): the maximum number of items that can fit
                in the jetpack. Defaults to 2.
            fuel (int): the amount of fuel in the jetpack's tank.
                Defaults to 10.

        Returns:
            A jetpck object with no contents and 10 units of fuel.
        """
        Backpack.__init__(self, name, color, max_size)
        self.fuel = fuel

    def fly(self, amount):
        """Fly by using 'amount' units of fuel."""
        if amount > self.fuel:                      # Check current fuel
            print("Not enough fuel!")
        else:
            self.fuel -= amount

    def dump(self):
        """Empty the contents of the jetpack and dump out all the fuel."""
        Backpack.dump(self)                         # Or self.contents = []
        self.fuel = 0                               # Reset fuel to 0


# Problem 4
class ComplexNumber(object):
    """Complex number object. Has a real and imaginary part.

    Attributes:
        real (float): the real part of the complex number.
        imag (float): the imaginary part of the complex number.
    """
    def __init__(self, a, b):
        """Initialize (separately) the real and imaginary components.
        Inputs:
            a (float): the real part.
            b (float): the imaginary part.
        """
        self.real = a
        self.imag = b

    def conjugate(self):
        """Return a ComplexNumber object of the complex conjugate."""
        return ComplexNumber(self.real, -1*self.imag)

    def __abs__(self):
        """Return the magnitude of the complex number.
        |a+bi| = sqrt{a^2 + b^2}.
        """
        return sqrt(self.real**2 + self.imag**2)

    def __lt__(self, other):
        """(a+bi) < (c+di) iff |a+bi| < |c+di|."""
        return abs(self) < abs(other)

    def __gt__(self, other):
        """(a+bi) > (c+di) iff |a+bi| > |c+di|."""
        return abs(self) > abs(other)

    def __eq__(self, other):
        """(a+bi) = (c+di) iff a=c AND b=d."""
        return self.real == other.real and self.imag == other.imag

    def __ne__(self, other):
        """(a+bi) != (c+di) iff a!=c OR b!=d."""
        return not self == other            # or, more explicitly,
        return self.real != other.real or self.imag != other.imag

    def __add__(self, other):
        """(a+bi) + (c+di) = (a+c) + (b+d)i"""
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        """(a+bi) - (c+di) = (a-c) + (b-d)i"""
        return ComplexNumber(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        """(a+bi)*(c+di) = (ac-bd) + (ad+bc)i"""
        real = (self.real * other.real) - (self.imag * other.imag)
        imag = (self.real * other.imag) + (self.imag * other.real)
        return ComplexNumber(real, imag)

    def __div__(self,other):
        """Do a little algebra before implementing:
        (a+bi) / (c+di)
        = (a+bi)*(c-di) / (c+di)*(c-di)             # Multiply by the conjugate
        = ((ac+bd) + (bc-ad)i) / (c**2 + d**2)      # Distribute
        """
        denom = float(other.real**2 + other.imag**2)
        real = ((self.real * other.real) + (self.imag * other.imag))/denom
        imag = ((self.imag * other.real) - (self.real * other.imag))/denom
        return ComplexNumber(real, imag)
