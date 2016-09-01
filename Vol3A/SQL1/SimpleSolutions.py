# Name this file 'solutions.py'.
"""Volume III Lab : SQL1.
This is a solutions file that is closer to what the students will actually turn
in.  It should have the same answers but in a less robust and less clean format.
This can be used as a tool to understand the solutions.py
"""
import sqlite3 as sql
import csv

def droptables():
    db = sql.connect("sql1")
    cur = db.cursor()
    cur.execute('DROP TABLE MajorInfo')
    cur.execute('DROP TABLE CourseInfo')
    cur.execute('DROP TABLE StudentInformation')
    cur.execute('DROP TABLE StudentGrades')
    
    

# Problem 1
def new_tables():
    """ Create two tables in the database "sql1".  Call the first table
    MajorInfo with columns MajorCode(int) and MajorName(string).  Call the
    second table CourseInfo with columns CourseID(int) and CourseName(string).    
    """
    db = sql.connect("sql1")
    cur = db.cursor()
    cur.execute('CREATE TABLE MajorInfo (MajorCode INTEGER, MajorName TEXT);')
    cur.execute('CREATE TABLE CourseInfo (CourseID INT, CourseName TEXT);')
    cur.execute("PRAGMA table_info('MajorInfo')")
    for info in cur:
        print info
    db.commit()
    db.close()

# Problem 2
def icd9tables():
    """ Create a table called ICD in the database sql2.  Import the data from
    icd9.csv.  There should be 4 columns: id(int),gender(text), age(int), and
    codes (string).
    """
    
    with open('icd9.csv','rb') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',')]
    db = sql.connect("sql2")
    cur = db.cursor()
    
    cur.execute("CREATE TABLE ICD (id INTEGER, gender TEXT, age INTEGER, codes TEXT)")
    cur.executemany("INSERT INTO ICD VALUES (?,?,?,?);",rows)
    db.commit()
    db.close()

# Problem 3
def sampletables():
    """ Create a table from the data given in the lab in the sql1 database."""
    studentinfo = [(401767594, 'Michelle Fernandez',  1 ),
    (678665086 , 'Gilbert Chapman', 1 ),
    (53725811 , 'Roberta Cook' , 2 ),
    (886308195 , 'Rene Cross' , 3 ),
    (103066521 , 'Cameron Kim' , 4 ),
    (821568627 , 'Mercedes Hall' , 3 ),
    (206208438 , 'Kristopher Tran' , 2 ),
    (341324754 , 'Cassandra Holland' , 1 ),
    (262019426 , 'Alfonso Phelps' , 3 ),
    (622665098 , 'Sammy Burke' ,2 )]
    majorinfo = [(1,"Math"),(2,"Science"),(3,"Writing"),(4,"Art")]
    studentgrades = [(401767594,4,'C'),
    (401767594,3,'B'),
    (678665086,4,'A'),
    (678665086,3,'A'),
    (553725811,2,'C'),
    (678665086,1,'B'),
    (886308195,1,'A'),
    (103066521,2,'C'),
    (103066521,3,'C'),
    (821568627,4,'D'),
    (821568627,2,'A'),
    (821568627,1,'B'),
    (206208438,2,'A'),
    (206208438,1,'C'),
    (341324754,2,'D'),
    (341324754,1,'A'),
    (103066521,4,'A'),
    (262019426,2,'B'),
    (262019426,3,'C'),
    (622665098,1,'A'),
    (622665098,2,'A')]
    
    courseinfo = [(1, 'Calculus'),(2,'English'),(3,'Pottery'),(4,'History')]
    
    db = sql.connect("sql1")
    cur = db.cursor()
    
    cur.execute("CREATE TABLE StudentInformation (StudentID INTEGER, Name TEXT,MajorCode INTEGER)")
    cur.executemany("INSERT INTO StudentInformation VALUES (?,?,?);",studentinfo)
    cur.executemany("INSERT INTO MajorInfo VALUES (?,?);",majorinfo)
    cur.execute("CREATE TABLE StudentGrades (StudentID INTEGER, ClassID INTEGER, Grade TEXT)")
    cur.executemany("INSERT INTO StudentGrades VALUES (?,?,?);",studentgrades)
    cur.executemany("INSERT INTO CourseInfo VALUES (?,?);",courseinfo)

# Problem 4
def freqcodes():
    """ Using the ICD9 table that you created in problem 2.  How many men
    between the ages of 25 and 25 are there?  How many women between those
    same ages?  Return your answers as a tuple.
    """
    db = sql.connect("sql2")
    cur = db.cursor()
    cur.execute("SELECT * FROM ICD WHERE gender = 'M' AND age<=35 AND age>=25;")
    rowsM = cur.fetchall()
    cur.execute("SELECT * FROM ICD WHERE gender = 'F' AND age<=35 AND age>=25;")
    rowsF = cur.fetchall()
    return len(rowsM),len(rowsF)

if __name__ == "__main__":
    droptables()
    new_tables()
    #icd9tables()
    sampletables()
    #print freqcodes()
    
