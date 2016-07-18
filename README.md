# ManDup
A script I made in python to manipulate duplicate files in a directory. 
```
find-duplicates.py <drive> [-option]
```
For example, to list directory and files that are duplicates:
```
python find-duplicates.py G: --list
```
To move or delete files you would just use those options:
```
python find-duplicates.py G: --move
python find-duplicates.py G: --delete
```
