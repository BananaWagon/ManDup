import os
import sys
import shutil
import argparse
from time import sleep

from os.path import join, dirname, basename, getsize

parser = argparse.ArgumentParser(description = "A tool for manipulating duplicate files. Searches for duplicate file names only.",
                                usage = '%(prog)s <path> [option]')

parser.add_argument('path', help = 'The path to search for duplicates. Will search sub-directories as well.')
parser.add_argument('-l', '--list', action = 'store_true', help = 'List all the files that are duplicates. It will list by folder followed by duplicates in that folder.')
parser.add_argument('-m', '--move', action = 'store_true', help = 'Move all duplicates to destination folder.')
parser.add_argument('-d', '--delete', action = 'store_true', help = 'Delete all duplicates that are found. ')

args = parser.parse_args()

# TODO: Make a better way to implement an ignore list. 
ignore = frozenset([ 'Cover.jpg', 'AlbumArtSmall.jpg', 'Folder.jpg',
                'Thumbs.db',
                'desktop.ini',
                'REAM ME FIRST.txt', 'READ ME FIRST.txt', 'ReadMe.txt', 'readme.txt',
                '.BridgeSort', '.BridgeLabelsAndRatings', '\u2016'])


class DuplicateFinder(object):
    """Finds duplicate files in a folder or folders."""
    
    def __init__(self, path, destination = os.path.expanduser('F:\\moved')):
        self.path = path
        self.destination = destination
        #self.option = option
        self.current_file = ''
        self.file_index = set()
        self.file_dup_index = []
        self.dir_dup_index =[]
        self.moved = 0
        self.not_moved = 0
        self.deleted = 0
        self.total_size_index = 0
        self.total_size_moved = 0
        self.total_size_dup = 0
        self.total_size_deleted= 0
        
    
    def run(self):
        """List/Move/Delete files if file is a duplicate."""
        
        for self.current_file in self.locate_files():
            self.total_size_index += getsize(self.current_file)
            if basename(self.current_file) in self.file_index:
                self.add_to_dup_index()
            
                if args.list:
                    print("{len_seen_files}\t{0}".format(basename(self.current_file), len_seen_files = len(self.file_dup_index)))
                
                elif args.move:
                    self.move_file()
                                
                elif args.delete:
                    # sefl.total_size_deleted += getsize(self.current_file)
                    print(":Deleting:  {0}".format(basename(self.current_file)), end="\r")
                    if self.delete_file():
                        print("-=DELETED=-")                
                                        
            if basename(self.current_file) not in self.file_index:
                self.file_index.add(basename(self.current_file))
    
    
    def locate_files(self):
        """Parses all files in path including sub directories."""
        
        for (dirname, dirs, files) in os.walk(self.path):
            for filename in files:
                # Ignore files in this set
                if filename not in ignore:
                    # From what I can tell yield gives next in list without
                    # using a lot of memory.
                    yield join(dirname, filename)
            
            
    def add_to_dup_index(self):
        """Adds file names and directory names to a list."""
        
        self.total_size_dup += getsize(self.current_file)
        self.file_dup_index.append(dirname(self.current_file))
        if dirname(self.current_file) not in self.dir_dup_index:
            self.dir_dup_index.append(dirname(self.current_file))
            print("\nFolder:  {0}".format(dirname(self.current_file)))
            
            
    def move_file(self):
        """Moves all duplicate files in given path to destination"""
        
                # TODO: Make option to choose destination.
                #       Preserve the directory structure when moving. 
                #       Delete empty folders left behind.
        if args.move:
            print(":Moving:  {0}".format(basename(self.current_file)), end="\r")
            try:
                shutil.move(self.current_file, self.destination)
                self.moved += 1
            except Exception as e:
                if str(e) == 'Destination path \'' + join(self.destination, basename(self.current_file)) + '\' already exists':
                    print("!!! File already exists !!!")
                else:
                    print(e)
                self.not_moved += 1
            print("-=MOVED=-")
        
        
    def delete_file(self):
        """Deletes all duplicate files"""
        
        if args.delete:
            try:
                # TODO: os.remove does not reliably delete a file. Find out why.
                
                while os.path.isfile(self.current_file):
                    os.remove(self.current_file)
                    #Loop till removed
                self.deleted =+ 1
            except Exception as e:
                print(e) # print error string to catch specific exeptions 
                return False
        return True
    
            
    def stats(self):
        """Formats program metrics and prints to screen."""
        
        stats = """
            ..........................................
            {len_seen_files} original files on drive.
            {len_dir_dup_index} directories have duplicates.
            {len_file_dup_index} duplicate files.\tSize:  {len_total_size_dup} MB
            {total_files} total files on drive.\tSize:  {len_total_size} MB
            """.format(
            len_seen_files = len(self.file_index),
            len_dir_dup_index = len(self.dir_dup_index),
            len_file_dup_index = len(self.file_dup_index),
            len_total_size_dup = int(self.total_size_dup / 1000000),
            total_files = len(self.file_index) + len(self.file_dup_index),
            len_total_size = int(self.total_size_index / 1000000),
        )
        
        if args.move:
            stats += """
            {self.moved} duplicate files moved to:\t{self.destination}
            {self.not_moved} files not moved.""".format(self=self)
            
        if args.delete:
            stats += """
            {self.deleted} duplicate files deleted from:\t{self.path}""".format(self=self)
            
        return stats
    
    
df = DuplicateFinder(args.path)
df.run()
print(df.stats())






