import sqlite3 as sql
import random
import csv

dbfile = 'students.db'    
def get_conn():
    con = sql.connect(dbfile)
    return con

# prob:tablerelations (= one to one, =>/<= one to many/many to one, <=> many to many)
# StudentID=Name
# Name=>Grade (using grades)
# Name=>Classes (using classes)
# Name<=MajorCode (using majors)
# Name<=MinorCode (using majors)
# Majors.ID = Majors.Name
# Classes.ID = Classes.Name
# Grades.ClassID<=>Grades.Grade (Using Grades and Classes)
    
def studentmajors():
    con = get_conn()
    cur = con.cursor()
    
    try:
        cur.execute("""SELECT majors.name, COUNT(students.name) 
            FROM students LEFT OUTER JOIN majors ON students.majorcode=majors.id 
            GROUP BY students.majorcode ORDER BY majors.name ASC;""")
        results = cur.fetchall()
        cur.close()
        return results
    except:
        pass
    finally:
        con.close()
        
def studentGPA():
    con = get_conn()
    cur = con.cursor()
    
    try:
        cur.execute("""SELECT ROUND(AVG(
                        CASE WHEN grade IN ('A+', 'A', 'A-') THEN 4.0
                            WHEN grade IN ('B+', 'B', 'B-') THEN 3.0
                            WHEN grade IN ('C+', 'C', 'C-') THEN 2.0
                            WHEN grade IN ('D+', 'D', 'D-') THEN 1.0
                            ELSE 0.0
                        END), 2) AS grade
                    FROM students JOIN grades ON students.studentid=grades.studentid 
                    WHERE grade IS NOT NULL;""")
        result = cur.fetchall()
        cur.close()
        return result
    except:
        pass
    finally:
        con.close()
        
def likec():
    con = get_conn()
    cur = con.cursor()
    
    try:
        cur.execute("""SELECT students.name, majors.name 
            FROM students LEFT OUTER JOIN majors ON students.majorcode=majors.id 
            WHERE students.name LIKE '% C%';""")
        results = cur.fetchall()
        cur.close()
        return results
    except:
        pass
    finally:
        con.close()

def manygrades():
    con = get_conn()
    cur = con.cursor()
    
    try:
        cur.execute("""SELECT name, COUNT(*) 
                    FROM students JOIN grades ON students.studentid=grades.studentid 
                    WHERE grade IS NOT NULL GROUP BY name HAVING COUNT(*)>2;""")
        results = cur.fetchall()
        cur.close()
        return results
    except:
        pass
    finally:
        con.close()