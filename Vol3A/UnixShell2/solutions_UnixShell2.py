# solutions_UnixShell2.py
'''
Solutions for Volume 3, Lab 2: More on Unix Shell
Written Summer 2015
'''

# PROBLEM 1: Make count_files.py an executable script
'''
SHELL COMMANDS: (Executed in the Shell-Lab/Python directory)
$ which python
On the author's system, this was: /home/tanner/anaconda/bin/python

Open count_files.py and add the shebang at the first line of the file. One the 
   author's system, this was
#!/home/tanner/anaconda/bin/python

$ chmod ug+x count_files.py
'''

# PROBLEM 2:
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
    
    # PROBLEM 3: Implement find_file and find_word
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
    
    # PROBLEM 4: Implement largest_files
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
        
# PROBLEM 5: Secure copy with partner
'''
SHELL COMMAND:
(follow example boxes and just plug in system-specific information
'''        
        
# PROBLEM 6: Download files in urls.txt
'''
SHELL COMMAND: (Execute in Shell-Lab/Documents)
wget -i urls.txt
'''

# PROBLEM 7: Format using awk
'''
$ awk ' BEGIN{FS = "\t"};{ print $7,$9 } ' < files.txt | sort -r > date-modified.txt
'''
