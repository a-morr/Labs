#!/bin/bash

cd Shell2/

# Problem 1
echo \#\!/bin/bash > hello
echo echo \"Hello World\" >> hello

# # Problem 2
chmod u+x hello
./hello

# Problem 4
./Scripts/script1 &
./Scripts/script2 &
./Scripts/script3 &
jobs > Scripts/log

# Problem 8
wget -i Documents/urls.txt
mv *.* Photos/
