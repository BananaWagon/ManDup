import os
import sys
import shutil
import argparse

from os.path import join, dirname, basename, getsize

#http://stackoverflow.com/questions/7427101/dead-simple-argparse-example-wanted-1-argument-3-results

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
                'READ ME FIRST.txt', 'ReadMe.txt', 'readme.txt'])

class DuplicateFinder(object):
    """Finds duplicate files in a folder or folders."""
    
    def __init__(self, path, option, destination = os.path.expanduser('F:\\moved')):
        self.path = path
        self.destination = destination
        self.option = option
        self.current_file = ''
        self.file_index = set()
        self.file_dup_index = []
        self.dir_dup_index =[]
        self.moved = 0
        self.not_moved = 0
        self.deleded = 0
        self.total_size_index = 0
        self.total_size_moved = 0
        self.total_size_dup = 0
        self.total_size_deleted= 0
        
        
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
        
        self.total_size_dup += getsize(basename(self.current_file))
        self.file_dup_index.append(basename(self.current_file))
        if dirname not in self.dir_dup_index:
            self.dir_dup_index.append(dirname(self.current_file))
            print("\nFolder: {0}".format(dirname(self.current_file)))
            
            
    def move_file(self):
        """Moves all duplicate files in given path to destination"""
        
                # TODO: Make option to choose destination.
                #       Perserve the directory structure when moving. 
                #       Delete empty folders left behind.
        if args.move:
            try:
                print("Moving: {0}".format(self.current_file), end=" ... ")
                shutil.move(self.current_file, self.destination)
                print("-=MOVED=-")
            except Exception as e:
                print(e) # print error string to catch specific exceptions
                self.not_moved += 1
                # TODO: Validate file exists error
                print("!!! File already exists !!!")
        
    
    def delete_file(self):
        """Deletes all duplicate files"""
        
        if args.delete:
            try:
                print("Deleting: {0}".format(basename(self.current_file, end=" ... ")))
                # TODO: os.remove does not reliably delete a file. Find out why.
                os.remove(self.current_file)
                print("-=DELETED=-")
            except Exception as e:
                print(e) # print error string to catch specific exeptions 
                         # do something for specific error
    
    
    def run(self):
        """List/Move/Delete files if file is a duplicate."""
        
        for self.current_file in self.locate_files():
            if basename(self.current_file) in self.file_index:
                self.total_size += getsize(self.current_file)
                self.add_to_dup_index()
            
                if args.list:
                    print("    {0}".format(self.current_file))
                
                elif args.move:
                    self.moved =+ 1
                    self.move_file()
            
                elif args.delete:
                    self.deleted += 1
                    # sefl.total_size_deleted += getsize(self.current_file)
                    self.delete_file()
                
            if basename(self.current_file) not in self.file_index:
                self.file_index.add(basename(self.current_file))

                
    def stats(self):
        """Formats program metrics and prints to screen."""
        
        stats = """
            ..........................................
            {len_seen_files} total files on drive.
            {len_dir_dup_index} directories have duplicates.
            {len_file_duplist} duplicate files./tSize:  {total_size_indexed}
            """.format(
            len_seen_files = len(self.file_index),
            len_dir_duplist = len(self.dir_dup_index),
            len_file_dup_index = len(self.file_dup_index),
            len_total_size_dup = int(self.total_size_dup / 1000000000),
        )
        
        if args.move:
            stats += """
            {self.moved} duplicate files moved to:\t{self.destination}
            {self.not_moved} files not moved.""".format(self=self)
            
        if args.delete:
            stats += """
            {self.deleted} duplicate files deleted from:\t{self.path}
            """.format(self=self)
            
        return stats
        
    
out_path = os.path.join(dirname(os.path(__file__)), 'out_folder')

# args.??? parser does not give a single option. Find out how to pass option given. 
df = DuplicateFinder(args.path, args.???, destination = out_path)
df.run()
print(df.stats())






