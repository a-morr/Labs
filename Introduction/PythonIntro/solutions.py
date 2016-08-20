# solutions.py
"""Introductory Labs: Getting Started. Solutions file.
NOTE: For this Introductory lab, we recommend NOT providing a specifications
file so that they have to define the functions themselves.
"""

# Problem 1 (ungraded)
if __name__ == '__main__':
    print("Hello, world!")


# Problem 2
def sphere_volume(r):
    """Return the volume of the sphere of radius 'r'.
    Use 3.14159 for pi in your computation.
    """
    return (4 * 3.14159 / 3)*r**3


# Problem 3
def first_half(my_string):
    """Return the first half of the string 'my_string'. Exclude the
    middle character if there are an odd number of characters.

    Examples:
        >>> first_half("python")
        'pyt'
        >>> first_half("ipython")
        'ipy'
    """
    return my_string[:len(my_string)//2]

def backward(my_string):
    """Return the reverse of the string 'my_string'.

    Examples:
        >>> backward("python")
        'nohtyp'
        >>> backward("ipython")
        'nohtypi'
    """
    return my_string[::-1]


# Problem 4
def list_ops():
    """Define a list with the entries "bear", "ant", "dog", and "cat".
    Perform the following operations on the list:
        - Append "eagle".
        - Remove the entry at index 1.
        - Replace the entry at index 2 with "fox".
        - Append "fox".
    Return the resulting list.

    Examples:
        >>> list_ops()
        ['fox', 'eagle', 'dog', 'bear']
    """
    my_list = ["bear", "ant", "dog", "cat"]
    my_list.append("eagle")
    my_list[2] = "fox"
    my_list.pop(1)                  # or my_list.remove(my_list[1])
    my_list.sort()
    my_list = my_list[::-1]         # or my_list.reverse()
    return my_list


# Problem 5
def pig_latin(word):
    """Translate the string 'word' into Pig Latin

    Examples:
        >>> pig_latin("apple")
        'applehay'
        >>> pig_latin("banana")
        'ananabay'
    """
    if word[0] in "aeiou":
        return word + "hay"
    else:
        return word[1:] + word[0] + "ay"

# New Problem 6
def palindrome():
    """Find and retun the largest panindromic number made from the product
    of two 3-digit numbers.
    """
    winner = 0
    for n in xrange(100,1000):
        for m in xrange(n,1000):
            product = n*m
            num = str(product)
            if num == num[::-1] and product > winner:
                winner = product
    return winner

# Problem 7
def alt_harmonic(n):
    """Return the partial sum of the first n terms of the alternating
    harmonic series. Use this function to approximate ln(2).
    """
    return sum([(-1)**(i+1)/float(i) for i in xrange(1,n+1)])

