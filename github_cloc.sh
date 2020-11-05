#!/bin/bash
read -p "Who's repository is it (what's the username it's under) that you wish to count?" user
read -p "What's the name of the repository?:" repo


#Download
address='https://github.com/'$user'/'$repo'.git'
git clone --depth 1 $address

#Count it, and delete:
cloc $repo 
rm -rf $repo
