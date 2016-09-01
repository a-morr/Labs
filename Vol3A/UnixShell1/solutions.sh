#!/bin/bash

# Problem 1
cd Shell1/

# Problem 2
rm -r Audio/
mkdir Documents/ Photos/ Python/

# Problem 3
mv *.jpg Photos/
mv *.txt Documents/
mv *.py Python/

# Problem 4
find . -name "*.jpg" -exec mv {} Photos \;

# Problem 5
wc -w < Documents/words.txt > Documents/sortedwords.txt
cat Documents/words.txt | sort >> Documents/sortedwords.txt

# Problem 6
tar -zcvf Photos/pics.tar.gz Photos/*

# Problem 7-9
find . -name "*" > Documents/first_vim.txt
