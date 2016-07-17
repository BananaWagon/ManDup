import argparse

parser = argparse.ArgumentParser(description = "A tool for manipulating duplicate files. Searches for duplicate file names only.",
                                usage = '%(prog)s <path> [option]')

parser.add_argument('path', help = 'The path to search for duplicates. Will search sub-directories as well.')
parser.add_argument('-l', '--list', action = 'store_true', help = 'List all the files that are duplicates. It will list by folder followed by duplicates in that folder.')
parser.add_argument('-m', '--move', action = 'store_true', help = 'Move all duplicates to destination folder.')
parser.add_argument('-d', '--delete', action = 'store_true', help = 'Delete all duplicates that are found. ')

args = parser.parse_args()

parser.print_help()

if args.list:
    print('\n-list')
    print(args.list)
    print(args.path)

if args.move:
    print('\n-move')
    print(args.move)
    print(args.path)
    
if args.delete:
    print('\n-delete')
    print(args.list)
    print(args.path)
    
