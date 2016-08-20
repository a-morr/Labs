# Name this file 'solutions.py'.
"""Volume III Lab : SQL1.
<Name>
<Class>
<Date>
"""
import sqlite3 as sql
import csv

# Problem 1
def new_tables():
    """ Create two tables in the database "sql1".  Call the first table
    MajorInfo with columns MajorCode(int) and MajorName(string).  Call the
    second table CourseInfo with columns CourseID(int) and CourseName(string).    
    """
    raise NotImplementedError("Problem 1 Incomplete")

# Problem 2
def icd9tables():
    """ Create a table called ICD in the database sql2.  Import the data from
    icd9.csv.  There should be 4 columns: id(int),gender(text), age(int), and
    codes (string).
    """
    raise NotImplementedError("Problem 2 Incomplete")

# Problem 3
def sampletables():
    """ Create a table from the data given in the lab in the sql1 database."""
    raise NotImplementedError("Problem 3 Incomplete")
    
# Problem 4
def freqcodes():
    """ Using the ICD9 table that you created in problem 2.  How many men
    between the ages of 25 and 25 are there?  How many women between those
    same ages?  Return your answers as a tuple.
    """
    raise NotImplementedError("Problem 4 Incomplete")
