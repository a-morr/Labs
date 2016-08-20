#!/bin/bash

set -e                              # Exit as soon as one command fails.

if [ "$#" -ne 1 ]; then             # Check for a command line argument.
    echo -e "Provide the name of the branch to be deleted"
else                                # Delete the specified git branch.
    echo -e "\nAttempting to delete branch $1...\n"
    git checkout develop
    git pull upstream develop
    git push origin develop
    git checkout $1
    git merge develop
    git checkout develop
    git branch -d $1
    git push origin :$1
    # Clean up the repository by removing auxiliary files.
    set +e
    find . -name "*.pyc" -exec rm -f {} +
    rm -f Vol?.[^tex]* Vol?.toc
    rm -f ExtraLabs.[^tex]* ExtraLabs.toc
    rm -f InstructorNotes.[^tex]* InstructorNotes.toc

    echo -e "\nDone\n"
    git status
    git branch
fi
