# Python Udemy - Space Invaders

This is part of a Udemy course to build the classic Space Invaders game using PyGame.
The IntelliJ PyCharm IDE is primarily used for maintenance of this repo.

# Project Dependencies

```
$ sudo python3 -m ensurepip
$ pip3 --version
$ pip3 install pytest
$ pytest --version
$ pip3 install pylint

# Game Engine Dependencies
$ pip3 install pygame

# AI and Data Science Dependencies
$ pip3 install torch
$ pip3 install matplotlib
```

# PyCharm Interpreter Setup

To fix "unresolved references" errors in individual python packages, you'll need to right click directories with module imports, right click, and select "Mark Directory As... Sources Root"  

Inspect the `.idea/misc.xml` file and confirm that the jdk-name is "Python 3.7", and not "Python 3.7 (Project Name)".  

Inspect the `.idea/Project.iml` file and confirm there is an order entry for:  
```
<orderEntry type="jdk" jdkName="Python 3.7" jdkType="Python SDK" />
```

## Git Workflow References

Useful git commands for quickly traversing repos:  
```
# Display your git configuration
git config --list
git config --global -l

# Display all remote branches
git branch --remote

# Concise view of git history
git log --oneline

# Visual graph of git history
git log --oneline --graph --all --decorate --abbrev-commit

# See how many lines of code you've changed
git diff --shortstat --cached

# Delete a remote branch
git push origin :pr-merged-feature

# Preview your stashed changes
git stash list
git stash show -p stash@{1}

# Un-commit and stage changes from most recent commit
git reset --soft HEAD~1
```
