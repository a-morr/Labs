# Shell_solutions.py
'''
Solutions for Volume 3 Lab 1: Unix Shell
Written by Tanner Christensen, Summer 2015
'''


# PROBLEM 1: Navigate to Shell-Lab directory
'''
$ SHELL COMMANDS: (It's trivial. Free points awarded)
$ cd Downloads/Shell-Lab
'''

# PROBLEM 2: Delete Audio folder and its contents. Create Documents, Photos, and Python directories
'''
SHELL COMMANDS: (Executed in the Shell-Lab directory)
$ rm -r Audio 
$ mkdir Documents Photos Python
'''

# PROBLEM 3: Move *.jpg to Photos, *.txt to Documents, and *.py to Python
'''
SHELL COMMANDS: (Executed in the Shell-Lab directory)
$ mv *.jpg Photos
$ mv *.txt Documents
$ mv *.py Python
'''

# PROBLEM 4: Move the *.jpg files found deep in the the directory hierachy to Photos
'''
SHELL COMMANDS: (Executed in the Shell-Lab directory)
To find where the .jpg files are
$ find . -type f -name "*.jpg"

Then move each file with mv command
$ mv <filepath> Photos

More specifically,
$ mv Files/Dec/Holidays/*.jpg Photos
$ mv Files/Feb/pics/*.jpg Photos
$ mv Files/Apr/user/Sally/Alaska/*.jpg Photos
$ mv Files/Jul/Vacation/*.jpg Photos
'''

# PROBLEM 5: Count words and sort words in word.txt. Save output to sortedwords.txt
'''
SHELL COMMANDS: (Executed in the Shell-Lab/Documents directory)
$ wc -l < words.txt > sortedwords.txt
$ sort < words.txt >> sortedwords.txt
'''

# PROBLEM 6: Make count_files.py an executable script
'''
SHELL COMMANDS: (Executed in the Shell-Lab/Python directory)
$ which python
On the author's system, this was: /home/tanner/anaconda/bin/python

Open count_files.py and add the shebang at the first line of the file. One the 
   author's system, this was
#!/home/tanner/anaconda/bin/python

$ chmod ug+x count_files.py
'''

# PROBLEM 7:
'''
SHELL COMMANDS: (Executed in the Shell-Lab/Scripts directory
$ ./script1 &
$ ./script2 &
$ ./script3 &
$ jobs > log.txt
'''

import subprocess
import numpy as np
import scipy as sp

class Shell(object):
    def __init__(self):
        pass
    
    # PROBLEM 8: Implement find_file and find_word
    def find_file(self, filename, d=None):
        """
        Find a file inside a given directory.  By default, the search starts
        in the current directory.
        """        
        if d is None:
            d = "."
            
        command = "find " + d + " -name \"" + filename + "\""
        files = subprocess.check_output(command,shell=True).split('\n')
        files.pop()
        return files
        
    def find_word(self, word, d=None):
        """
        Search the contents of all the files within a directory for a given
        word.  By default, the search starts in the current directory
        """
        if d is None:
            d = "."

        command = "grep -nr " + word + " " + d
        files = subprocess.check_output(command,shell=True).split('\n')
        files.pop()
        return files
    
    # PROBLEM 9: Implement largest_files
    def largest_files(self,n,d=None):
        """
        Return a list of the n biggest files and their sizes. 
        By default, the search starts in the current directory
        """
        if d is None:
            d = '.'
        command = "find " + d + " -type f"
        files = subprocess.check_output(command, shell=True).split('\n')
        files.pop()
        split_files = np.array([subprocess.check_output('du ' + f, shell=True).strip().split('\t') for f in files]) 
        sizes = np.array(split_files[:,0],dtype=np.int32)
        sorted_index = sp.argsort(sizes)[::-1]
        return split_files[sorted_index][:n]
        
    # PROBLEM 10 (Optional): secure copy with partner
    
        
        
