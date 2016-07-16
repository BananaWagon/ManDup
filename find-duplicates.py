import os
import sys
import shutil

from os.path import join

# Boiler plate maybe?
drive = sys.argv[1]
option = sys.argv[2]

destination = os.path.expanduser('F:\\moved')

# TODO: Make a better way to implement an ignore list. 
ignore = frozenset([ 'Cover.jpg', 'AlbumArtSmall.jpg', 'Folder.jpg',
                'Thumbs.db',
                'desktop.ini',
                'READ ME FIRST.txt', 'ReadMe.txt', 'readme.txt'])

first_instance = set()
file_list = []
file_duplist = []
dir_list = []
dir_duplist = []
total_size = 0
not_moved = 0

for (dirname, dirs, files) in os.walk(drive):
    for filename in files:
        the_file = os.path.join(dirname, filename)
        
        # TODO: Move all this crap to funtions
        # Ignore files in this set
        if filename in ignore:
            continue
        
        # List/Move/Delete file if file is a duplicate
        elif str(filename) in first_instance:
            if not filename in file_duplist:                    
                if not dirname in dir_duplist:
                    dir_duplist.append(dirname)
                    print("\nFolder: " + dirname)
                file_duplist.append(filename)
                
                # List all duplicate files in the given path
                if option == "-list":
                    total_size += os.path.getsize(the_file)
                    print("    " + filename)
                    
                # Move all duplicate files in given path to destination
                # TODO: Make option to choose destination.
                #       Perserve the directory structure when moving. 
                #       Delete empty folders left behind. 
                if option == "-move":
                    try:
                        print("Moving: " + filename, end=" ... ")
                        shutil.move(the_file, destination)
                        print("-=MOVED=-")
                    except Exception as e:
                        not_moved += 1
                        # TODO: Validate file exists error
                        print("!!! File already exists !!!")
                
                # Delete all duplicate files in given path
                if option == "-delete":
                    try:
                        print("Deleting: " + filename, end=" ... ")
                        os.remove(the_file)
                        print("-=DELETED=-")
                    except Exception as e:
                        print(e)
                
        # Add file name to set and list if not in list
        if not filename in file_list:
            first_instance.add(str(filename))
            file_list.append(filename)

# Output when finished. 
# TODO: Put in function and use a text wrapper.
#       Change output based on option argv        
print("\n..........................................")

print("\n" + str(len(first_instance)) + " total files on drive.")
print(str(len(dir_duplist)) + " directories have duplicates.")
print(str(len(file_duplist)) + " duplicate files.\t" + "Size: " + str(int(total_size / 1000000000)))

if option == "-move":
    print(str(not_moved) + " duplicate files moved to:\t" + str(destination))








