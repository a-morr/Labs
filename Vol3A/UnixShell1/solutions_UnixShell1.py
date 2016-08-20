# solutions_UnixShell1.py
'''
Solutions for Volume 3, Lab 1: Unix Shell
Written Summer 2015
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

# PROBLEM 4: Count words and sort words in word.txt. Save output to sortedwords.txt
'''
SHELL COMMANDS: (Executed in the Shell-Lab/Documents directory)
$ wc -l < words.txt > sortedwords.txt
$ sort < words.txt >> sortedwords.txt
'''

# PROBLEM 5: Move the *.jpg files found deep in the the directory hierachy to Photos
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

# PROBLEM 6: Compress files in Photos directory
'''
SHELL COMMANDS: (Executed in Shell-Lab/)
$ tar -zcvf pics.tar.gz Photos/*
'''

# PROBLEM 7:
'''
SHELL COMMANDS: (Executed in Shell-Lab/Documents)
$ vim first_vim.txt
'''

# PROBLEM 8: Experiment with navigation
'''
VIM COMMANDS:
Use all the commands listed in the problem. I can't think of a way we would grade this.
'''

# PROBLEM 9: Copy/Paste, Cut/Paste
'''
VIM COMMANDS:
copy/paste: (in order)
  v - to enter visual mode
  hjkl - to select text
  y - to copy
  Esc - to return to command mode
  p - to paste
cut/paste: (in order)
  v - to enter visual mode
  hjkl - to select text 
  d - to cut
  Esc - to return to command mode
  p - to paste
'''

# PROBLEM 10: Save and exit
'''
VIM COMMANDS:
save and exit: (in order)
  :wq - save and exit
'''
